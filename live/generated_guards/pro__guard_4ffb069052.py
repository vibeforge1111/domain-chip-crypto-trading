def guard(features: dict, prediction: str) -> str:
    """Filter trades when broader 2-hour RSI conflicts with trade direction."""
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long trades when broader timeframe is deeply oversold (weak trend)
    if prediction == 'long' and rsi_2h < 32:
        return "skip"
    
    # Skip short trades when broader timeframe is deeply overbought (strong uptrend)
    if prediction == 'short' and rsi_2h > 68:
        return "skip"
    
    return prediction