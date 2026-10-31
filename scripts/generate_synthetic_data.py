"""Generate the synthetic SurveyML-Eval benchmark data bundle."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from surveymleval.generator import generate_all


def main() -> None:
    output_root = ROOT / "data" / "synthetic"
    generate_all(output_root)
    print(f"Synthetic data generated at: {output_root}")


if __name__ == "__main__":
    main()
