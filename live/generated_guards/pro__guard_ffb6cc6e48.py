def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using BB and Stochastic extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Long signals: skip if overbought (BB upper + Stochastic high)
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Short signals: skip if oversold (BB lower + Stochastic low)
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction