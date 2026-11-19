"""Find the single most dangerous data class in a breach."""
from .weights import DATA_CLASS_WEIGHTS


def get_primary_data_type(data_classes_str: str) -> str:
    """Return the highest-weight data class present (title-cased)."""
    if not isinstance(data_classes_str, str):
        return "Unknown"

    dcs = data_classes_str.lower()
    by_weight = sorted(DATA_CLASS_WEIGHTS,
                       key=DATA_CLASS_WEIGHTS.get, reverse=True)
    for cls in by_weight:
        if cls in dcs:
            return cls.title()
    return "Other"
