def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB position and Stochastic confirm overbought/oversold extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: BB at upper band (>85%) and stochastic confirms (>80)
    if bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Oversold: BB at lower band (<15%) and stochastic confirms (<20)
    if bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction