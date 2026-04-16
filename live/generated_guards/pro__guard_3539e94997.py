def guard(features: dict, prediction: str) -> str:
    """Filter signals where RSI extremes conflict with momentum direction."""
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    
    # Skip longs when overbought with weakening momentum
    if prediction == 'long' and rsi > 65 and momentum < -0.1:
        return 'skip'
    
    # Skip shorts when oversold with strengthening momentum
    if prediction == 'short' and rsi < 35 and momentum > 0.1:
        return 'skip'
    
    return prediction