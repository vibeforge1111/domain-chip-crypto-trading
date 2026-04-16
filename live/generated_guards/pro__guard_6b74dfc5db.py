def guard(features: dict, prediction: str) -> str:
    """Filter entries against broader trend using 2-hour RSI alignment."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when broader trend is overbought (>75) to avoid counter-trend entries
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    # Skip shorts when broader trend is oversold (<25) to avoid counter-trend entries
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction