"""Risk tier (1-4) per breach: severity blended with scale."""


def get_risk_tier(score: float, pwn_millions: float) -> int:
    """60% severity + 40% scale (100M+ people = full scale)."""
    scale_score = min(pwn_millions / 100, 1.0)
    combined = 0.6 * (score / 10) + 0.4 * scale_score
    if combined >= 0.75:
        return 4
    elif combined >= 0.50:
        return 3
    elif combined >= 0.25:
        return 2
    else:
        return 1
