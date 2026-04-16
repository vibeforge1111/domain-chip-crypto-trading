def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position and Stochastic extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Skip long when overbought (upper BB + stoch above 80)
    if prediction == "long" and bb_pct_b > 0.92 and stoch_k > 80:
        return "skip"
    
    # Skip short when oversold (lower BB + stoch below 20)
    if prediction == "short" and bb_pct_b < 0.08 and stoch_k < 20:
        return "skip"
    
    return prediction