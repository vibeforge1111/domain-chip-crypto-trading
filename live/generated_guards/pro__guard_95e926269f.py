def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger position and Stochastic extremes with 2h RSI confirmation."""
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long: reject if overbought on BB, Stoch, AND 2h RSI
    if prediction == "long":
        if bb_pct > 0.85 and stoch_k > 80 and rsi_2h > 65:
            return "skip"
    
    # Short: reject if oversold on BB, Stoch, AND 2h RSI
    if prediction == "short":
        if bb_pct < 0.15 and stoch_k < 20 and rsi_2h < 35:
            return "skip"
    
    return prediction