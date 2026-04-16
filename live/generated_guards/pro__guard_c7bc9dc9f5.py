def guard(features: dict, prediction: str) -> str:
    """Reject signals where RSI extreme conflicts with EMA trend direction."""
    rsi = features.get('rsi_14', 50)
    ema_slope = features.get('ema_slope', 0)
    
    # Long: skip if RSI overbought AND EMA not bullish
    if prediction == 'long' and rsi > 70 and ema_slope < 0.001:
        return 'skip'
    
    # Short: skip if RSI oversold AND EMA not bearish
    if prediction == 'short' and rsi < 30 and ema_slope > -0.001:
        return 'skip'
    
    return prediction