def guard(features: dict, prediction: str) -> str:
    """Detect overbought/oversold extremes using BB position and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: both BB at upper band and Stochastic in overbought zone
    if bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Oversold: both BB at lower band and Stochastic in oversold zone
    if bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction