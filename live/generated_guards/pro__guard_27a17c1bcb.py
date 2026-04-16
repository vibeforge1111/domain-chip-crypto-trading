def guard(features: dict, prediction: str) -> str:
    """Filter trades when both Bollinger Band position and Stochastic confirm extremes."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Both indicators overbought: reject longs
    if prediction == "long" and bb_pct > 0.88 and stoch_k > 80 and stoch_d > 70:
        return "skip"
    
    # Both indicators oversold: reject shorts
    if prediction == "short" and bb_pct < 0.12 and stoch_k < 20 and stoch_d < 30:
        return "skip"
    
    return prediction