"""Maps a breach's domain to an industry (first keyword match wins)."""

DOMAIN_INDUSTRY = {
    # Social media
    "linkedin": "Social Media", "facebook": "Social Media",
    "twitter": "Social Media", "instagram": "Social Media",
    "myspace": "Social Media", "tumblr": "Social Media",
    "snapchat": "Social Media", "reddit": "Social Media",
    # Software / cloud
    "adobe": "Software/Tech", "microsoft": "Software/Tech",
    "canva": "Software/Tech", "dropbox": "Cloud Storage",
    "lastpass": "Cloud Storage", "slack": "Software/Tech",
    # E-commerce
    "ebay": "E-Commerce", "amazon": "E-Commerce",
    "shopify": "E-Commerce", "etsy": "E-Commerce",
    # Email / telecom
    "yahoo": "Email/Telecom", "hotmail": "Email/Telecom",
    "aol": "Email/Telecom", "att": "Email/Telecom",
    # Gaming
    "zynga": "Gaming", "steam": "Gaming", "sony": "Gaming",
    "minecraft": "Gaming", "epicgames": "Gaming",
    # Finance
    "paypal": "Finance", "capitalone": "Finance",
    "equifax": "Finance", "experian": "Finance",
    # Healthcare
    "optum": "Healthcare", "anthem": "Healthcare",
    "labcorp": "Healthcare",
    # Education
    "chegg": "Education", "coursera": "Education",
}


def map_industry(domain: str) -> str:
    """Return the industry for a domain, or 'Other' if unknown."""
    d = str(domain).lower()
    for key, industry in DOMAIN_INDUSTRY.items():
        if key in d:
            return industry
    return "Other"
