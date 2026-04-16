def guard(features: dict, prediction: str) -> str:
    """Filter trades when both Bollinger Band position and Stochastic confirm extreme conditions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Reject long when overbought (bb upper band + stoch >85)
    if prediction == "long" and bb_pct_b > 0.95 and stoch_k > 85:
        return "skip"
    
    # Reject short when oversold (bb lower band + stoch <15)
    if prediction == "short" and bb_pct_b < 0.05 and stoch_k < 15:
        return "skip"
    
    return prediction