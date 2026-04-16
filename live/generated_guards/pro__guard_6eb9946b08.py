def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration via MACD histogram."""
    macd_histogram = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        # MACD histogram near zero or negative = bullish momentum weakening
        if macd_histogram <= 0.001:
            return 'skip'
        # Wider timeframe not supportive of longs
        if rsi_2h < 45:
            return 'skip'
    
    elif prediction == 'short':
        # MACD histogram near zero or positive = bearish momentum weakening
        if macd_histogram >= -0.001:
            return 'skip'
        # Wider timeframe not supportive of shorts
        if rsi_2h > 55:
            return 'skip'
    
    return prediction