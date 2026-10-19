
from pathlib import Path

from evallab.evaluate import run_evaluation
from evallab.report import save_report


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
REPORT_PATH = PROJECT_ROOT / "reports" / "evaluation_report.json"


def main() -> None:
    report = run_evaluation(DATA_DIR)
    save_report(report, REPORT_PATH)

    print(f"Evaluated {report['dataset_size']} cases.")
    print("Summary metrics:")

    for name, value in report["metrics"].items():
        print(f"  {name}: {value:.4f}")

    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
