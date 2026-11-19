"""Flag breaches that leaked credentials or financial secrets."""

CREDENTIAL_KEYWORDS = [
    "password", "credit card", "bank account",
    "social security", "financial transaction", "auth token",
]


def tag_credential_leak(data_classes_str: str) -> int:
    """Return 1 if any credential keyword appears, else 0."""
    dcs = str(data_classes_str).lower()
    return int(any(kw in dcs for kw in CREDENTIAL_KEYWORDS))
