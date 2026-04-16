def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum decelerates against position direction using macd_histogram."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs if MACD shows bearish momentum deceleration and not oversold
    if prediction == 'long' and macd < -0.0002 and stoch_k > 30:
        return "skip"
    
    # Skip shorts if MACD shows bullish momentum deceleration and not overbought
    if prediction == 'short' and macd > 0.0002 and stoch_k < 70:
        return "skip"
    
    return prediction