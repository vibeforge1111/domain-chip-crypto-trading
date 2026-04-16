def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict the 2-hour broader trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Don't fight the broader 2h trend
    # Long entries only when 2h RSI shows bullish regime
    if prediction == 'long' and rsi_2h < 45:
        return 'skip'
    # Short entries only when 2h RSI shows bearish regime
    if prediction == 'short' and rsi_2h > 55:
        return 'skip'
    
    return prediction