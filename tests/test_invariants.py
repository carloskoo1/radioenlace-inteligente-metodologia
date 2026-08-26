import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def test_reference_summary():
    s = json.loads((ROOT / "results/tables/analysis_summary.json").read_text(encoding="utf-8"))
    assert s["raw_files"] == 90
    assert s["raw_ap_rows"] == 173_513
    assert s["master_observed_minutes"] == 118_458
    assert s["anomaly_flags"] == 1_093
