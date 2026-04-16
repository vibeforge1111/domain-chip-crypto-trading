def guard(features: dict, prediction: str) -> str:
    """Filter trades where MACD histogram shows momentum deceleration against trade direction."""
    macd_hist = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs: skip if momentum is bearish (histogram negative) and 2h RSI not oversold
    if prediction == 'long' and macd_hist < 0 and rsi_2h > 30:
        return "skip"
    
    # For shorts: skip if momentum is bullish (histogram positive) and 2h RSI not overbought
    if prediction == 'short' and macd_hist > 0 and rsi_2h < 70:
        return "skip"
    
    return prediction