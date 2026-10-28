"""Tests sin tocar la base de adquisición; se crea una SQLite sintética temporal."""
from datetime import datetime
from pathlib import Path
import sqlite3
import tempfile
import unittest

from dashboard.live_source import read_recent_ap


class TestReadOnlyLiveSource(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "test.db"
        conn = sqlite3.connect(self.path)
        conn.execute("""CREATE TABLE radio_link_local (
            id INTEGER PRIMARY KEY, timestamp_local TEXT, radio_role TEXT,
            sta_dl_rssi REAL, snr_dl REAL, mcs_dl REAL, dl_rate REAL,
            error TEXT)""")
        conn.execute("""CREATE TABLE radio_link_config_telemetry (
            id INTEGER PRIMARY KEY, timestamp_local TEXT,
            frequency_band TEXT, channel_bandwidth_mhz REAL)""")
        t = datetime.now().astimezone().isoformat()
        conn.execute("INSERT INTO radio_link_local VALUES (1,?, 'AP',-74,23,204,103,'')", (t,))
        conn.execute("INSERT INTO radio_link_local VALUES (2,?, 'SM',-60,25,210,110,'')", (t,))
        conn.execute("INSERT INTO radio_link_config_telemetry VALUES (1,?,'6_GHZ',20)", (t,))
        conn.commit()
        conn.close()

    def tearDown(self):
        self.tmp.cleanup()

    def test_only_ap(self):
        x = read_recent_ap(self.path)
        self.assertEqual(x["status"], "fresh")
        self.assertEqual(len(x["rows"]), 1)
        self.assertEqual(x["rows"][0]["rssi_dl_dbm"], -74)
        self.assertEqual(x["config"]["frequency_band"], "6_GHZ")

    def test_absent_source(self):
        self.assertEqual(read_recent_ap(None)["status"], "unconfigured")
        self.assertEqual(read_recent_ap(str(self.path) + "missing")["status"], "missing")

    def test_stale_detected(self):
        with sqlite3.connect(self.path) as c:
            c.execute("UPDATE radio_link_local SET timestamp_local='2026-01-01T00:00:00-05:00'")
        self.assertEqual(read_recent_ap(self.path)["status"], "stale")


if __name__ == "__main__":
    unittest.main()
