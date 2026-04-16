def guard(features: dict, prediction: str) -> str:
    """Filter trades where broader 2h trend contradicts prediction direction."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Align longs with bullish 2h context
    if prediction == 'long' and rsi_2h < 45:
        return 'skip'
    # Align shorts with bearish 2h context
    if prediction == 'short' and rsi_2h > 55:
        return 'skip'
    return prediction