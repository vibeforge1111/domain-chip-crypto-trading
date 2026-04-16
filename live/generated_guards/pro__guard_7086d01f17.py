def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # Stochastic bullish crossover: k above d, d in oversold zone
        if not (stoch_k > stoch_d and stoch_d < 30):
            return "skip"
        # Price should be above or near VWAP for longs
        if vwap_dev < -0.005:
            return "skip"
        # Wider timeframe should not be bearish
        if rsi_2h < 35:
            return "skip"
    
    elif prediction == "short":
        # Stochastic bearish crossover: k below d, d in overbought zone
        if not (stoch_k < stoch_d and stoch_d > 70):
            return "skip"
        # Price should be below or near VWAP for shorts
        if vwap_dev > 0.005:
            return "skip"
        # Wider timeframe should not be bullish
        if rsi_2h > 65:
            return "skip"
    
    return prediction