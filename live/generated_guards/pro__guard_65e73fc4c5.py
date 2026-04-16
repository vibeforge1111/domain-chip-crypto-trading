def guard(features: dict, prediction: str) -> str:
    """Filter trades that contradict Bollinger Band extreme signals."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only take longs near lower band, only take shorts near upper band
    if prediction == "long" and bb_pct_b > 0.90:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.10:
        return "skip"
    
    return prediction