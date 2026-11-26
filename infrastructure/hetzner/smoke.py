"""Bounded Hetzner lifecycle and synthetic compute smoke test."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.hetzner.cloud/v1"
OWNER = "ela-smoke-v1"
LOCATION = "nbg1"
SERVER_TYPE = "ccx33"
LEASE_SECONDS = 45 * 60
NAME = re.compile(r"ela-smoke-[0-9]+-[0-9]+\Z")


class Cloud:
    def __init__(self, token):
        if not token:
            raise ValueError("HCLOUD_TOKEN is missing")
        self.token = token

    def request(self, method, path, payload=None, missing_ok=False):
        request = urllib.request.Request(
            API + path,
            data=None if payload is None else json.dumps(payload).encode(),
            headers={"Authorization": f"Bearer {self.token}",
                     "Content-Type": "application/json"},
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                body = response.read()
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as error:
            if missing_ok and error.code == 404:
                return None
            # API responses may contain secrets; log status only.
            raise RuntimeError(f"Hetzner {method} {path.split('?')[0]}: HTTP {error.code}") from None

    def managed(self, kind):
        page = 1
        while page is not None:
            query = urllib.parse.urlencode(
                {"label_selector": f"managed-by={OWNER}", "page": page})
            result = self.request("GET", f"/{kind}?{query}")
            yield from result[kind]
            page = result["meta"]["pagination"]["next_page"]


def owned(resource, name=None, now=None):
    labels = resource.get("labels", {})
    candidate = resource.get("name", "")
    if not NAME.fullmatch(candidate) or labels.get("managed-by") != OWNER:
        return False
    if labels.get("run-name") != candidate:
        return False
    if name is not None:
        return candidate == name
    expiry = labels.get("expires-at", "")
    return expiry.isdigit() and int(expiry) <= now


def wait_until(predicate, seconds):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(5)
    raise TimeoutError("Resource did not reach expected state")


def cleanup(cloud, name=None, now=None):
    """Remove only resources with the exact pilot name and ownership labels."""
    if name is None and now is None:
        now = int(time.time())
    for kind in ("servers", "primary_ips", "ssh_keys"):
        for resource in list(cloud.managed(kind)):
            if not owned(resource, name, now):
                continue
            resource_id = resource["id"]
            path = f"/{kind}/{resource_id}"
            if kind == "primary_ips":
                # Server deletion and automatic IP deletion can settle separately.
                def detached_or_gone():
                    current = cloud.request("GET", path, missing_ok=True)
                    return current is None or current.get("primary_ip", current).get("assignee_id") is None

                wait_until(detached_or_gone, 90)
            cloud.request("DELETE", path, missing_ok=True)
            wait_until(lambda: cloud.request("GET", path, missing_ok=True) is None, 60)

    def no_remaining():
        return not any(
            owned(item, name, now)
            for kind in ("servers", "primary_ips", "ssh_keys")
            for item in cloud.managed(kind)
        )

    wait_until(no_remaining, 60)
    print("Cleanup verified: no matching pilot resources remain.", flush=True)


def labels_for(name, now, lease_seconds=LEASE_SECONDS):
    if not NAME.fullmatch(name):
        raise ValueError("Invalid pilot run name")
    return {"managed-by": OWNER, "run-name": name,
            "expires-at": str(now + lease_seconds)}


def check_price(cloud):
    from decimal import Decimal
    result = cloud.request("GET", f"/server_types?name={SERVER_TYPE}")
    types = result["server_types"]
    if len(types) != 1:
        raise RuntimeError("Could not confirm server type")
    matches = [p for p in types[0]["prices"] if p["location"] == LOCATION]
    if len(matches) != 1:
        raise RuntimeError("Could not confirm location price")
    hourly = Decimal(matches[0]["price_hourly"]["gross"])
    if not Decimal("0") < hourly <= Decimal("0.29"):
        raise RuntimeError("Hourly server rate exceeds the approved estimate")
    print(f"Confirmed server rate: EUR {hourly}/hour gross, plus IPv4.", flush=True)


BENCHMARK = """
import hashlib, json, os, platform, shutil, time
from concurrent.futures import ProcessPoolExecutor

def work(index):
    block = bytes([index]) * (1024 * 1024)
    digest = hashlib.sha256()
    for _ in range(256):
        digest.update(block)
    return digest.hexdigest()

if __name__ == '__main__':
    start = time.monotonic()
    serial = [work(i) for i in range(8)]
    serial_seconds = time.monotonic() - start
    start = time.monotonic()
    with ProcessPoolExecutor(max_workers=8) as pool:
        parallel = list(pool.map(work, range(8)))
    parallel_seconds = time.monotonic() - start
    if serial != parallel:
        raise RuntimeError('Synthetic results do not match')
    print(json.dumps({
        'architecture': platform.machine(),
        'logical_cpus': os.cpu_count(),
        'memory_bytes': os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE'),
        'disk_free_bytes': shutil.disk_usage('/').free,
        'serial_seconds': serial_seconds,
        'parallel_seconds': parallel_seconds,
        'matching_sha256': serial,
        'synthetic_only': True,
    }))
"""


def run(cloud, name, output, workload=None, lease_seconds=LEASE_SECONDS):
    if any(resource for kind in ("servers", "primary_ips", "ssh_keys")
           for resource in cloud.managed(kind)):
        raise RuntimeError("A managed pilot resource exists. Clean it up first.")
    check_price(cloud)
    labels = labels_for(name, int(time.time()), lease_seconds)
    start = time.monotonic()
    try:
        with tempfile.TemporaryDirectory() as directory:
            key = Path(directory) / "ssh"
            subprocess.run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "",
                            "-f", str(key)], check=True, timeout=20)
            ssh_key = cloud.request("POST", "/ssh_keys", {
                "name": name, "public_key": key.with_suffix(".pub").read_text().strip(),
                "labels": labels,
            })["ssh_key"]
            address = cloud.request("POST", "/primary_ips", {
                "name": name, "type": "ipv4", "location": LOCATION,
                "auto_delete": True, "labels": labels,
            })["primary_ip"]
            server = cloud.request("POST", "/servers", {
                "name": name, "server_type": SERVER_TYPE, "location": LOCATION,
                "image": "ubuntu-24.04", "ssh_keys": [ssh_key["id"]],
                "labels": labels, "start_after_create": True,
                "public_net": {"enable_ipv4": True, "ipv4": address["id"],
                               "enable_ipv6": False},
            })["server"]
            server_id = server["id"]
            wait_until(lambda: cloud.request("GET", f"/servers/{server_id}")["server"]["status"] == "running", 180)
            host = address["ip"]
            ssh = ["ssh", "-i", str(key), "-o", "BatchMode=yes",
                   "-o", "StrictHostKeyChecking=accept-new",
                   "-o", f"UserKnownHostsFile={directory}/known_hosts",
                   "-o", "ConnectTimeout=5", f"root@{host}"]
            def ready():
                result = subprocess.run(ssh + ["true"], capture_output=True, timeout=15)
                return result.returncode == 0
            wait_until(ready, 180)
            if workload is not None:
                workload(ssh, output)
                return
            result = subprocess.run(ssh + ["cloud-init status --wait >/dev/null && python3 -"],
                                    input=BENCHMARK, text=True, capture_output=True,
                                    timeout=240, check=True)
            report = json.loads(result.stdout)
            if not report["synthetic_only"] or len(report["matching_sha256"]) != 8:
                raise RuntimeError("Invalid synthetic output")
            report["elapsed_seconds_including_boot"] = time.monotonic() - start
            output.write_text(json.dumps(report, indent=2) + "\n")
            print("Synthetic compute result validated.", flush=True)
    finally:
        cleanup(cloud, name=name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("run", "cleanup", "expire"))
    parser.add_argument("--name")
    parser.add_argument("--output", type=Path, default=Path("hetzner-smoke.json"))
    args = parser.parse_args()
    cloud = Cloud(os.environ.get("HCLOUD_TOKEN"))
    if args.mode in ("run", "cleanup") and not NAME.fullmatch(args.name or ""):
        parser.error("--name must be an exact pilot run name")
    if args.mode == "run":
        run(cloud, args.name, args.output)
    elif args.mode == "cleanup":
        cleanup(cloud, name=args.name)
    else:
        cleanup(cloud)


if __name__ == "__main__":
    main()
