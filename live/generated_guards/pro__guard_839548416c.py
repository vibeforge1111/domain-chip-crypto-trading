def guard(features: dict, prediction: str) -> str:
    """Guard based on Bollinger Band position extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow entries at BB extremes
    if prediction == "long" and bb_pct_b >= 0.10:
        return "skip"
    if prediction == "short" and bb_pct_b <= 0.90:
        return "skip"
    
    return prediction