def guard(features: dict, prediction: str) -> str:
    """Filter countertrend trades - reject longs when overbought, shorts when oversold."""
    ema_slope = features.get('ema_slope', 0)
    rsi_14 = features.get('rsi_14', 50)
    
    # Uptrend but overbought
    if ema_slope > 0 and rsi_14 > 70:
        return 'skip'
    # Downtrend but oversold  
    if ema_slope < 0 and rsi_14 < 30:
        return 'skip'
    
    return prediction