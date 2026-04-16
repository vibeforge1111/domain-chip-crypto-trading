def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes and confirmations."""
    bb_pct = features.get("bb_pct_b", 0.5)
    
    # Skip longs when price is too extended near upper band
    if prediction == "long" and bb_pct > 0.95:
        return "skip"
    # Skip shorts when price is too extended near lower band
    if prediction == "short" and bb_pct < 0.05:
        return "skip"
    
    # Confirm with VWAP alignment
    vwap_dev = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap_dev < -0.003:
        return "skip"
    if prediction == "short" and vwap_dev > 0.003:
        return "skip"
    
    # Stochastic confirmation to avoid reversal traps
    stoch = features.get("stoch_k", 50)
    if prediction == "long" and stoch > 85:
        return "skip"
    if prediction == "short" and stoch < 15:
        return "skip"
    
    return prediction