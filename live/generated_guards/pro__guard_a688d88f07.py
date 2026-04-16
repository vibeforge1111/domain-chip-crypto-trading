def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject longs when overbought (both indicators confirm)
    if prediction == "long" and stoch_k > 80 and bb_pct_b > 0.85:
        return "skip"
    
    # Reject shorts when oversold (both indicators confirm)
    if prediction == "short" and stoch_k < 20 and bb_pct_b < 0.15:
        return "skip"
    
    return prediction