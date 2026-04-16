def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    bb_pct = features.get("bb_pct_b", 0.5)
    
    # Only allow trades at extreme BB positions (high-confidence zones)
    if prediction == "long" and bb_pct >= 0.05:
        return "skip"
    if prediction == "short" and bb_pct <= 0.95:
        return "skip"
    
    return prediction