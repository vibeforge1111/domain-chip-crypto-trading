def guard(features: dict, prediction: str) -> str:
    """Mean-reversion timing guard using RSI and stochastic extremes."""
    rsi = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    stoch = features.get('stoch_k', 50)
    
    # For longs: require oversold confirmation (RSI or stoch extreme)
    if prediction == "long":
        if rsi > 35 and stoch > 25:
            return "skip"
    
    # For shorts: require overbought confirmation (RSI or stoch extreme)
    if prediction == "short":
        if rsi < 65 and stoch < 75:
            return "skip"
    
    return prediction