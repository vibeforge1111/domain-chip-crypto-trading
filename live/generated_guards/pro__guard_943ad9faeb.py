def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions with confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # Require oversold BB position with confirming stochastics
        if bb_pct_b >= 0.05 or stoch_k >= 30:
            return "skip"
    elif prediction == "short":
        # Require overbought BB position with confirming stochastics
        if bb_pct_b <= 0.95 or stoch_k <= 70:
            return "skip"
    
    return prediction