def guard(features: dict, prediction: str) -> str:
    """Reject trades at Bollinger Band + Stochastic extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long at upper band with overbought stoch → reject
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Short at lower band with oversold stoch → reject
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction