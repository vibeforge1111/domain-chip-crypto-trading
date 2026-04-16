def guard(features: dict, prediction: str) -> str:
    """Filter trades with conflicting momentum signals."""
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Momentum deceleration check - reject longs with bearish MACD + overbought
    if prediction == "long" and macd < -0.0002 and stoch > 75:
        return "skip"
    
    # Momentum deceleration check - reject shorts with bullish MACD + oversold
    if prediction == "short" and macd > 0.0002 and stoch < 25:
        return "skip"
    
    return prediction