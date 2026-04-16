def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2-hour RSI."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs: reject if broader trend is bearish (rsi_2h < 35) 
    # or overbought (rsi_2h > 75 - limited upside room)
    if prediction == "long" and (rsi_2h < 35 or rsi_2h > 75):
        return "skip"
    
    # For shorts: reject if broader trend is bullish (rsi_2h > 65)
    # or deeply oversold (rsi_2h < 25 - bounce reversal risk)
    if prediction == "short" and (rsi_2h > 65 or rsi_2h < 25):
        return "skip"
    
    return prediction