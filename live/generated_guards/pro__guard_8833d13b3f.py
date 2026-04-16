def guard(features: dict, prediction: str) -> str:
    """Custom guard using Bollinger Band extremes and confirmation filters."""
    bb = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Only trade in high-confidence BB extreme zones
    if bb >= 0.05 and bb <= 0.95:
        return "skip"
    
    # Reject long when stoch confirms oversold (wait for bounce)
    if prediction == "long" and stoch_k < 20:
        return "skip"
    
    # Reject short when stoch confirms overbought (wait for dump)
    if prediction == "short" and stoch_k > 80:
        return "skip"
    
    # Additional vwap confirmation for entries
    if prediction == "long" and vwap_dev < -0.005:
        return "skip"
    if prediction == "short" and vwap_dev > 0.005:
        return "skip"
    
    return prediction