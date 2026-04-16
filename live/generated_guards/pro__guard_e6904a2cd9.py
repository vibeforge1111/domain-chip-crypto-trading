def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow longs at extreme lower band (<0.05)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    
    # Only allow shorts at extreme upper band (>0.95)
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction