def guard(features: dict, prediction: str) -> str:
    # Skip if momentum is decelerating against the trade direction
    macd = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Momentum deceleration: MACD histogram turning negative for longs or positive for shorts
    if prediction == "long" and macd < -0.0002:
        return "skip"
    if prediction == "short" and macd > 0.0002:
        return "skip"
    
    # Broader 2h timeframe overbought/oversold conditions
    if prediction == "long" and rsi_2h > 72:
        return "skip"
    if prediction == "short" and rsi_2h < 28:
        return "skip"
    
    return prediction