def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum deceleration using MACD histogram."""
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if MACD histogram negative (momentum deceleration)
    if macd < -0.0002:
        return "skip"
    
    # Skip if overbought with weakening momentum
    if stoch > 75 and macd < 0:
        return "skip"
    
    # Skip if wider timeframe RSI extended and momentum fading
    if rsi_2h > 70 and macd < 0:
        return "skip"
    
    return prediction