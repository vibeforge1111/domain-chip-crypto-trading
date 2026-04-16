def guard(features: dict, prediction: str) -> str:
    """Filter trades using broader 2h RSI trend alignment."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # For longs, require broader trend not in oversold territory
    if prediction == 'long' and rsi_2h < 42:
        return 'skip'
    
    # For shorts, require broader trend not in overbought territory
    if prediction == 'short' and rsi_2h > 58:
        return 'skip'
    
    return prediction