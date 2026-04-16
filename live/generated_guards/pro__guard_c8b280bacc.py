def guard(features: dict, prediction: str) -> str:
    """Custom guard function using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Stochastic crossover timing with RSI confirmation
    if prediction == "long":
        # Bullish: K crosses above D from oversold, confirmed by 2h trend
        if not (stoch_k > stoch_d and stoch_k < 30 and rsi_2h > 50):
            return "skip"
    
    if prediction == "short":
        # Bearish: K crosses below D from overbought, confirmed by 2h downtrend
        if not (stoch_k < stoch_d and stoch_k > 70 and rsi_2h < 50):
            return "skip"
    
    return prediction