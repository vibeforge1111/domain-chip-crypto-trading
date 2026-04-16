def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # Stochastic bullish crossover timing: k crosses below d in oversold
        if not (stoch_k < stoch_d and stoch_k < 40):
            return "skip"
        # Price should be near or above VWAP
        if vwap_dev < -0.002:
            return "skip"
        # 2h RSI shouldn't be overbought
        if rsi_2h > 70:
            return "skip"
    
    elif prediction == "short":
        # Stochastic bearish crossover timing: k crosses above d in overbought
        if not (stoch_k > stoch_d and stoch_k > 60):
            return "skip"
        # Price should be near or below VWAP
        if vwap_dev > 0.002:
            return "skip"
        # 2h RSI shouldn't be oversold
        if rsi_2h < 30:
            return "skip"
    
    return prediction