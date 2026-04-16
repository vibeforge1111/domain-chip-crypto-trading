def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum against direction."""
    macd = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long if MACD histogram is negative (bearish momentum)
    if prediction == 'long' and macd < -0.0003:
        return 'skip'
    
    # Skip short if MACD histogram is positive (bullish momentum)
    if prediction == 'short' and macd > 0.0003:
        return 'skip'
    
    # Additional filter: avoid longs when 2h RSI is overbought
    if prediction == 'long' and rsi_2h > 70:
        return 'skip'
    
    # Additional filter: avoid shorts when 2h RSI is oversold
    if prediction == 'short' and rsi_2h < 30:
        return 'skip'
    
    return prediction