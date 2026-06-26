
import time
import breach_pipeline
import nlp_tagger
import risk_scorer

def main():
    print("=" * 55)
    print("  BREACH TRACKER — Full Pipeline")
    print("=" * 55)

    t0 = time.time()

    print("\n── STEP 1: Fetch & Clean ──────────────────────────────")
    breach_pipeline.main()

    print("\n── STEP 2: NLP Severity Tagging ───────────────────────")
    nlp_tagger.main()

    print("\n── STEP 3: Risk Scoring + Excel Export ────────────────")
    risk_scorer.main()

    elapsed = time.time() - t0
    print("=" * 55)
    print(f"  Pipeline complete in {elapsed:.1f}s")
    print("  → data/breaches_final.xlsx is ready for Power BI")
    print("=" * 55)

if __name__ == "__main__":
    main()
