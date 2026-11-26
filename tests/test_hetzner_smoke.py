import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "hetzner_smoke", Path(__file__).resolve().parents[1] / "infrastructure/hetzner/smoke.py"
)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class DelayedCloud:
    """A deleted server's primary IP can remain assigned in API responses."""
    def __init__(self, name):
        labels = smoke.labels_for(name, 1000)
        self.rows = {
            "servers": [{"id": 1, "name": name, "labels": labels}],
            "primary_ips": [
                {"id": 2, "name": name, "labels": labels, "assignee_id": 1},
                {"id": 4, "name": "unrelated", "labels": {}, "assignee_id": 99},
            ],
            "ssh_keys": [{"id": 3, "name": name, "labels": labels}],
        }
        self.ip_reads = 0
        self.deleted = []

    def managed(self, kind):
        return iter(self.rows[kind])

    def request(self, method, path, missing_ok=False):
        kind, resource_id = path.strip("/").split("/")
        resource_id = int(resource_id)
        entries = self.rows[kind]
        item = next((row for row in entries if row["id"] == resource_id), None)
        if method == "DELETE":
            if kind == "primary_ips" and item and item["assignee_id"] is not None:
                raise AssertionError("IP deleted while still assigned")
            self.deleted.append((kind, resource_id))
            self.rows[kind] = [row for row in entries if row["id"] != resource_id]
            return {}
        if kind == "primary_ips" and item and resource_id == 2:
            self.ip_reads += 1
            if self.ip_reads == 3:
                item["assignee_id"] = None
            return {"primary_ip": item}
        return None if item is None else {kind[:-1]: item}


class HetznerCleanupTest(unittest.TestCase):
    def test_ip_detaches_after_server_deletion(self):
        name = "ela-smoke-123-1"
        cloud = DelayedCloud(name)
        with patch.object(smoke.time, "sleep", lambda _: None):
            smoke.cleanup(cloud, name=name)
            smoke.cleanup(cloud, name=name)
        self.assertEqual(cloud.ip_reads, 3)
        self.assertEqual(
            cloud.deleted, [("servers", 1), ("primary_ips", 2), ("ssh_keys", 3)]
        )
        self.assertEqual([row["id"] for row in cloud.rows["primary_ips"]], [4])
