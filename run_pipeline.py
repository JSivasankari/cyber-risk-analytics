"""Run the full pipeline: fetch -> tag -> score -> Excel export."""
import time

from breach_tracker.ingest import pipeline as ingest
from breach_tracker.tagging import pipeline as tagging
from breach_tracker.risk import pipeline as risk


def main():
    print("=" * 55)
    print("  BREACH TRACKER — Full Pipeline")
    print("=" * 55)

    t0 = time.time()

    print("\n── STEP 1: Fetch & Clean ──────────────────────────────")
    ingest.main()

    print("\n── STEP 2: NLP Severity Tagging ───────────────────────")
    tagging.main()

    print("\n── STEP 3: Risk Scoring + Excel Export ────────────────")
    risk.main()

    elapsed = time.time() - t0
    print("=" * 55)
    print(f"  Pipeline complete in {elapsed:.1f}s")
    print("  → data/breaches_final.xlsx is ready for Power BI")
    print("=" * 55)


if __name__ == "__main__":
    main()
