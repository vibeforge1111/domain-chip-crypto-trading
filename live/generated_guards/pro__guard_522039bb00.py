def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position extremes with VWAP confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Only allow trades at BB extremes (<0.05 or >0.95)
    if bb_pct_b < 0.05 and prediction == "long" and vwap_dev < 0:
        return prediction
    if bb_pct_b > 0.95 and prediction == "short" and vwap_dev > 0:
        return prediction
    
    return "skip"