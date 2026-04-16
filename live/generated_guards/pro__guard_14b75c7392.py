def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only take long signals near lower band (<0.05)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    
    # Only take short signals near upper band (>0.95)
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction