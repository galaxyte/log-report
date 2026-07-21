import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _ground_truth():
    """Independently re-derive the correct report values from the raw log."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_report_exists_and_is_valid_json():
    """Success criterion 1: /app/report.json exists and contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    json.loads(REPORT_PATH.read_text())


def test_total_requests_correct():
    """Success criterion 2: total_requests equals the true request count."""
    expected = _ground_truth()
    report = json.loads(REPORT_PATH.read_text())
    assert report.get("total_requests") == expected["total_requests"]


def test_unique_ips_correct():
    """Success criterion 3: unique_ips equals the true number of distinct client IPs."""
    expected = _ground_truth()
    report = json.loads(REPORT_PATH.read_text())
    assert report.get("unique_ips") == expected["unique_ips"]


def test_top_path_correct():
    """Success criterion 4: top_path equals the actual most-requested path."""
    expected = _ground_truth()
    report = json.loads(REPORT_PATH.read_text())
    assert report.get("top_path") == expected["top_path"]
