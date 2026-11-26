"""Fixed, fail-closed contract for the authorized two-library technical pilot."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "reports/prjdb19918-metadata-intake-20261126/input_manifest.json"
MANIFEST_SHA = "668591eb1e0127d742f2bc748cffb29558b97c8161766674cce8af75d6d0a0a3"
ROSTER = {"DRR631712": ("SCR2", "scramble", "SAMD00858914", 5482638623),
          "DRR631715": ("KD1", "tdp43_kd", "SAMD00858917", 4867330852)}
LEASE_SECONDS = 3 * 3600
REMOTE_SECONDS = 140 * 60
MAX_RATE = Decimal("0.32")


def select(run, path=MANIFEST):
    if run not in ROSTER:
        raise ValueError("Unapproved library")
    raw = Path(path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
        raise ValueError("Input manifest digest mismatch")
    manifest = json.loads(raw)
    matches = [x for x in manifest["libraries"] if x["run"] == run]
    if len(matches) != 1:
        raise ValueError("Expected one manifest record")
    row = matches[0]
    label, condition, sample, size = ROSTER[run]
    if (row["label"], row["condition"], row["sample"]) != (label, condition, sample):
        raise ValueError("Library identity mismatch")
    mates = row["mates"]
    if len(mates) != 2 or [m["mate"] for m in mates] != [1, 2]:
        raise ValueError("Expected ordered mates")
    if sum(m["bytes"] for m in mates) != size:
        raise ValueError("Pair size mismatch")
    for m in mates:
        expected = f"https://ftp.sra.ebi.ac.uk/vol1/fastq/DRR631/{run}/{run}_{m['mate']}.fastq.gz"
        if m["url"] != expected or not re.fullmatch(r"[0-9a-f]{32}", m["md5"]) or not 0 < m["bytes"] < 4_000_000_000:
            raise ValueError("Invalid input identity")
    return row


def combined_rate(cloud, location="nbg1", server_type="ccx33"):
    # Read only: closed on unexpected/missing price schema, currency or ambiguity.
    pricing = cloud.request("GET", "/pricing")["pricing"]
    if pricing["currency"].upper() != "EUR":
        raise RuntimeError("Non-EUR pricing")
    def rate(group, kind, value):
        rows = [r for r in pricing[group] if r[kind] == value]
        if len(rows) != 1:
            raise RuntimeError("Ambiguous price type")
        locs = [p for p in rows[0]["prices"] if p["location"] == location]
        if len(locs) != 1:
            raise RuntimeError("Ambiguous price location")
        x = Decimal(locs[0]["price_hourly"]["gross"])
        if not x.is_finite() or x < 0:
            raise RuntimeError("Invalid price")
        return x
    server = rate("server_types", "name", server_type)
    ip = rate("primary_ips", "type", "ipv4")
    if not (0 < server <= Decimal("0.29") and server + ip <= MAX_RATE):
        raise RuntimeError("Combined gross rate exceeds pilot allowance")
    return {"currency": "EUR", "server_rate_gross": str(server), "ipv4_rate_gross": str(ip),
            "combined_rate_gross": str(server + ip), "nominal_six_hours_eur": str(6 * (server + ip)),
            "not_hard_billing_cap": True}


def validate_result(obj, row):
    if obj.get("run") != row["run"] or obj.get("sample") != row["sample"] or obj.get("complete") is not True:
        raise ValueError("Missing or mismatched result")
    counts, qc = obj["counts"], obj["qc"]
    if set(counts) != {"canonical", "cryptic_left", "cryptic_right"}:
        raise ValueError("Unexpected event set")
    keys = {"sam_records", "alignment_groups", "eligible_groups", "marked_duplicate_records", "rejected_groups"}
    if set(qc) != keys or any(type(v) is not int or v < 0 for v in [*counts.values(), *qc.values()]):
        raise ValueError("Invalid count or QC field")
    if qc["alignment_groups"] != qc["eligible_groups"] + qc["rejected_groups"] or any(v > qc["eligible_groups"] for v in counts.values()):
        raise ValueError("QC accounting mismatch")
    if qc["sam_records"] < 2*qc["eligible_groups"] or qc["eligible_groups"] <= 0 or qc["marked_duplicate_records"] > 2*qc["eligible_groups"]:
        raise ValueError("No eligible evidence or inconsistent record count")
    if counts["canonical"] <= 0:
        raise ValueError("No canonical positive control; do not continue automatically")
    return obj
