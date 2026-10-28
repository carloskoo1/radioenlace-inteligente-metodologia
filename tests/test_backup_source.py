"""Pruebas con respaldos ZIP sintéticos. Nunca toca las copias reales de AtmosLink."""
import csv
import io
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile, ZIP_DEFLATED
from datetime import datetime

from dashboard.backup_source import read_recent_backup


class BackupSourceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.zip = self.root / "backup_CU01_20261028_061956.zip"
        stream = io.StringIO(newline="")
        fieldnames = ["rf_timestamp_local", "frequency_band", "field_analysis_valid",
                      "collection_status", "dl_rssi_dbm", "dl_snr_db", "dl_mcs",
                      "reported_dl_link_rate_mbps"]
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for band, valid, time, rssi in [
            ("6_GHZ", "1", "2026-10-28T05:55:00-05:00", "-74"),
            ("6_GHZ", "1", "2026-10-28T05:56:00-05:00", "-73"),
            ("5_GHZ", "1", "2026-10-28T05:57:00-05:00", "-70"),
            ("6_GHZ", "0", "2026-10-28T05:58:00-05:00", "-71")
        ]:
            writer.writerow({"rf_timestamp_local": time, "frequency_band": band,
                             "field_analysis_valid": valid,
                             "collection_status": "LINK_OPERATIONAL_DUAL",
                             "dl_rssi_dbm": rssi, "dl_snr_db": "23",
                             "dl_mcs": "204", "reported_dl_link_rate_mbps": "103"})
        with ZipFile(self.zip, "w", ZIP_DEFLATED) as z:
            z.writestr("scientific_campaign_6g_integrated.csv", stream.getvalue())

    def tearDown(self):
        self.tmp.cleanup()

    def test_reads_only_valid_6ghz_rows(self):
        r = read_recent_backup(self.root, limit=10)
        self.assertEqual(r["status"], "backup")
        self.assertEqual(len(r["rows"]), 2)
        self.assertEqual(r["rows"][-1]["rssi_dl_dbm"], "-73")
        self.assertEqual(r["last_timestamp"], "2026-10-28T05:56:00-05:00")

    def test_missing_directory(self):
        r = read_recent_backup(self.root / "not_found")
        self.assertEqual(r["status"], "missing")

    def test_does_not_change_zip(self):
        before = self.zip.read_bytes()
        read_recent_backup(self.root)
        self.assertEqual(before, self.zip.read_bytes())


if __name__ == "__main__":
    unittest.main()
