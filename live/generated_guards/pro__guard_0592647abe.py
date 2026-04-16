def guard(features: dict, prediction: str) -> str:
    """Mean-reversion timing guard for crypto 15-min reversal entries."""
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Long reversal: require oversold extremes
        oversold = rsi_14 < 32 or stoch_k < 28
        wide_oversold = rsi_2h < 40
        if not (oversold or wide_oversold):
            return "skip"
    elif prediction == "short":
        # Short reversal: require overbought extremes
        overbought = rsi_14 > 68 or stoch_k > 72
        wide_overbought = rsi_2h > 60
        if not (overbought or wide_overbought):
            return "skip"
    
    return prediction