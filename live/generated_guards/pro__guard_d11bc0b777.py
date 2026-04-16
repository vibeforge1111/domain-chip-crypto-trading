def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip longs when both BB and Stoch are overbought and above VWAP
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80 and vwap_dev > 0.01:
        return "skip"
    
    # Skip shorts when both BB and Stoch are oversold and below VWAP
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20 and vwap_dev < -0.01:
        return "skip"
    
    return prediction