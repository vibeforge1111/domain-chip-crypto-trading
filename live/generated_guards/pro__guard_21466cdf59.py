def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # High-confidence entries only at BB extremes
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction