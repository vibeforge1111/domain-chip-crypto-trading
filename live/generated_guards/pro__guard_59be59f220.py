def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2-hour RSI context."""
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long' and rsi_2h < 40:
        return 'skip'
    if prediction == 'short' and rsi_2h > 60:
        return 'skip'
    
    return prediction