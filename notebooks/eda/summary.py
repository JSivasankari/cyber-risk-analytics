"""Print the dataset shape and headline metrics."""


def run(df):
    print(f"Shape : {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("== Key metrics ==")
    print(f"Total breaches          : {len(df):,}")
    print(f"Date range              : {df['BreachDate'].min().date()} "
          f"→ {df['BreachDate'].max().date()}")
    print(f"Total people affected   : {df['PwnMillions'].sum():.1f}M")
    print(f"Avg breach size         : {df['PwnMillions'].mean():.2f}M")
    print(f"Median disclosure lag   : "
          f"{df['DisclosureLagDays'].median():.0f} days")
    print(f"Credential leak breaches: {df['IsCredentialLeak'].sum()} "
          f"({df['IsCredentialLeak'].mean()*100:.1f}%)")
