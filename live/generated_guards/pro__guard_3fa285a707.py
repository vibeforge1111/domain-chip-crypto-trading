def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme overbought/oversold conditions using BB position and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: BB near upper band + stochastic in overbought zone → reject longs
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Oversold: BB near lower band + stochastic in oversold zone → reject shorts
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction