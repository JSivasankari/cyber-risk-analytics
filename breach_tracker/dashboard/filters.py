"""Apply the sidebar selections to the breach table."""


def apply_filters(df, sel_years, sel_severity, sel_industry):
    """Return the rows matching every sidebar filter."""
    return df[
        (df["Year"] >= sel_years[0]) &
        (df["Year"] <= sel_years[1]) &
        (df["SeverityLabel"].isin(sel_severity)) &
        (df["Industry"].isin(sel_industry))
    ].copy()
