def guard(features: dict, prediction: str) -> str:
    """Reject trades when BB position and Stochastic align on extremes."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Overbought: BB near upper band + stoch overbought + 2h also overbought
    if prediction == "long" and bb_pct > 0.90 and stoch_k > 80 and rsi_2h > 65:
        return "skip"
    
    # Oversold: BB near lower band + stoch oversold + 2h also oversold
    if prediction == "short" and bb_pct < 0.10 and stoch_k < 20 and rsi_2h < 35:
        return "skip"
    
    return prediction