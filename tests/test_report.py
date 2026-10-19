
import json

from evallab.report import save_report


def test_save_report_writes_valid_json(tmp_path):
    report = {
        "dataset_size": 1,
        "metrics": {"abstention_accuracy": 1.0},
        "results": [{"question_id": "eval001"}],
    }

    output_path = tmp_path / "reports" / "evaluation_report.json"

    save_report(report, output_path)

    assert output_path.exists()

    with output_path.open("r", encoding="utf-8") as file:
        saved_report = json.load(file)

    assert saved_report == report
