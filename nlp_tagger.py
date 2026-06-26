
import pandas as pd
import os

DATA_CLASS_WEIGHTS = {
   
    "passwords":                    10,
    "password hints":               6,
    "security questions and answers": 7,
    "auth tokens":                  8,
   
    "credit cards":                 10,
    "bank account numbers":         10,
    "partial credit card data":     7,
    "financial transactions":       9,
   
    "social security numbers":      10,
    "government issued ids":        10,
    "tax identification numbers":   9,
    "passport numbers":             9,
    "driving license numbers":      8,
    
    "medical records":              10,
    "health insurance information": 9,
    "physical disabilities":        8,
    "mental health records":        9,
   
    "sexual orientations":          9,
    "sexual fetishes":              9,
    "political views":              7,
    "religious beliefs":            7,
    "dates of birth":               6,
    "ethnicities":                  6,
   
    "phone numbers":                5,
    "physical addresses":           5,
    "email addresses":              4,
   
    "ip addresses":                 3,
    "device information":           3,
    "geographic locations":         4,
    "browser user agent details":   2,
    "website activity":             3,
   
    "usernames":                    2,
    "names":                        2,
    "genders":                      2,
    "ages":                         2,
    "time zones":                   1,
    "spoken languages":             1,
    "employers":                    3,
    "job titles":                   2,
    "profile photos":               3,
    "avatars":                      1,
    "bios":                         2,
    "education levels":             2,
    "marital statuses":             3,
}


MAX_SCORE = sum(sorted(DATA_CLASS_WEIGHTS.values(), reverse=True)[:5])


def compute_severity_score(data_classes_str: str) -> float:
   
    if not isinstance(data_classes_str, str) or not data_classes_str.strip():
        return 0.0

    dcs = data_classes_str.lower()
    raw_score = sum(
        weight for cls, weight in DATA_CLASS_WEIGHTS.items() if cls in dcs
    )
    normalized = min(raw_score / MAX_SCORE * 10, 10.0)
    return round(normalized, 2)


def tag_severity_label(score: float) -> str:
  
    if score >= 7.0:   return "Critical"
    elif score >= 4.5: return "High"
    elif score >= 2.0: return "Medium"
    else:              return "Low"


def tag_credential_leak(data_classes_str: str) -> int:
 
    keywords = [
        "password", "credit card", "bank account",
        "social security", "financial transaction", "auth token"
    ]
    dcs = str(data_classes_str).lower()
    return int(any(kw in dcs for kw in keywords))


def get_primary_data_type(data_classes_str: str) -> str:
   
    if not isinstance(data_classes_str, str):
        return "Unknown"

    dcs = data_classes_str.lower()
   
    for cls in sorted(DATA_CLASS_WEIGHTS, key=DATA_CLASS_WEIGHTS.get, reverse=True):
        if cls in dcs:
           
            return cls.title()
    return "Other"


def get_risk_tier(score: float, pwn_millions: float) -> int:
   
    scale_score = min(pwn_millions / 100, 1.0)  # 100M+ = full scale
    combined    = 0.6 * (score / 10) + 0.4 * scale_score
    if combined >= 0.75:   return 4
    elif combined >= 0.50: return 3
    elif combined >= 0.25: return 2
    else:                  return 1


def main():
    input_path  = os.path.join("data", "breaches_clean.csv")
    output_path = os.path.join("data", "breaches_tagged.csv")

    print("[1/3] Loading clean breach data...")
    df = pd.read_csv(input_path)
    print(f"      ✓ {len(df)} records loaded")

    print("[2/3] Applying NLP severity tagging...")
    df["SeverityScore"]    = df["DataClassesStr"].apply(compute_severity_score)
    df["SeverityLabel"]    = df["SeverityScore"].apply(tag_severity_label)
    df["IsCredentialLeak"] = df["DataClassesStr"].apply(tag_credential_leak)
    df["PrimaryDataType"]  = df["DataClassesStr"].apply(get_primary_data_type)
    df["RiskTier"]         = df.apply(
        lambda r: get_risk_tier(r["SeverityScore"], r.get("PwnMillions", 0)), axis=1
    )

    
    print(f"      ✓ Severity distribution:")
    for label in ["Critical", "High", "Medium", "Low"]:
        n = (df["SeverityLabel"] == label).sum()
        print(f"          {label:10s}: {n:4d} ({n/len(df)*100:.1f}%)")

    cred_pct = df["IsCredentialLeak"].mean() * 100
    print(f"      ✓ Credential leaks: {cred_pct:.1f}% of all breaches")

    print(f"[3/3] Saving tagged data → {output_path}")
    df.to_csv(output_path, index=False)
    print(f"\n✅ nlp_tagger.py complete. Run risk_scorer.py next.")

    return df


if __name__ == "__main__":
    main()
