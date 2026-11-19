"""Combines every category into DATA_CLASS_WEIGHTS.

The merge order matters: ties in weight are broken by this order
when picking the 'primary' data type of a breach.
"""
from .credentials import CREDENTIALS
from .financial import FINANCIAL
from .identity import IDENTITY
from .health import HEALTH
from .personal import PERSONAL
from .contact import CONTACT
from .technical import TECHNICAL
from .profile import PROFILE

DATA_CLASS_WEIGHTS = {
    **CREDENTIALS, **FINANCIAL, **IDENTITY, **HEALTH,
    **PERSONAL, **CONTACT, **TECHNICAL, **PROFILE,
}
