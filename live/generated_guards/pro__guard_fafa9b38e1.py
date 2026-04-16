def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject longs when overbought on both BB and Stoch
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Reject shorts when oversold on both BB and Stoch
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction