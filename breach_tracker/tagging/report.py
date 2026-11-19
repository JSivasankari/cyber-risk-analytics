"""Console summary printed after tagging."""


def print_tag_summary(df):
    """Show severity split and credential-leak share."""
    print("      ✓ Severity distribution:")
    for label in ["Critical", "High", "Medium", "Low"]:
        n = (df["SeverityLabel"] == label).sum()
        print(f"          {label:10s}: {n:4d} ({n/len(df)*100:.1f}%)")
    cred_pct = df["IsCredentialLeak"].mean() * 100
    print(f"      ✓ Credential leaks: {cred_pct:.1f}% of all breaches")
