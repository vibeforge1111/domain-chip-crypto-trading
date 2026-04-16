def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating (macd_histogram near zero)."""
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if momentum is flattening near zero (deceleration zone)
    if abs(macd) < 0.0003:
        return "skip"
    
    # Skip long if histogram fading AND overbought 2h RSI
    if prediction == 'long' and macd > 0 and rsi_2h > 70:
        return "skip"
    
    # Skip short if histogram fading AND oversold 2h RSI
    if prediction == 'short' and macd < 0 and rsi_2h < 30:
        return "skip"
    
    return prediction