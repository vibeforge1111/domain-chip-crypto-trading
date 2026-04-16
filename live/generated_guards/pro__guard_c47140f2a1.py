def guard(features: dict, prediction: str) -> str:
    """Filter trades against the broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # In bullish 2h context, reject shorts
    if rsi_2h > 55 and prediction == 'short':
        return 'skip'
    
    # In bearish 2h context, reject longs
    if rsi_2h < 45 and prediction == 'long':
        return 'skip'
    
    return prediction