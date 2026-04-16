def guard(features: dict, prediction: str) -> str:
    """Filter trades when macd_histogram shows momentum deceleration against direction."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when bearish macd momentum (momentum deceleration)
    if prediction == "long" and macd < -0.0003:
        return "skip"
    
    # Skip shorts when bullish macd momentum (momentum deceleration)
    if prediction == "short" and macd > 0.0003:
        return "skip"
    
    # Additional filter: overbought/oversold contradicts trade direction
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    # Higher timeframe RSI confirming momentum loss
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction