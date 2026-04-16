def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject longs when overbought (BB upper band + stochastic overbought)
    if prediction == "long" and bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    # Reject shorts when oversold (BB lower band + stochastic oversold)
    if prediction == "short" and bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction