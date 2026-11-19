"""Severity score (0-10) and label from the data classes leaked."""
from .weights import DATA_CLASS_WEIGHTS

# Score of the 5 heaviest data classes = "maximum possible" breach.
MAX_SCORE = sum(sorted(DATA_CLASS_WEIGHTS.values(), reverse=True)[:5])


def compute_severity_score(data_classes_str: str) -> float:
    """Sum matched keyword weights, normalised to a 0-10 scale."""
    if not isinstance(data_classes_str, str) or not data_classes_str.strip():
        return 0.0

    dcs = data_classes_str.lower()
    raw_score = sum(
        weight for cls, weight in DATA_CLASS_WEIGHTS.items() if cls in dcs
    )
    normalized = min(raw_score / MAX_SCORE * 10, 10.0)
    return round(normalized, 2)


def tag_severity_label(score: float) -> str:
    """Bucket a severity score into Critical / High / Medium / Low."""
    if score >= 7.0:
        return "Critical"
    elif score >= 4.5:
        return "High"
    elif score >= 2.0:
        return "Medium"
    else:
        return "Low"
