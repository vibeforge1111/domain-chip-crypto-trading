def guard(features: dict, prediction: str) -> str:
    """Guard against RSI extremes in weak trends and Bollinger exhaustion moves."""
    rsi = features.get('rsi_14', 50)
    trend_strength = features.get('trend_strength', 0.5)
    bb_position = features.get('bb_position', 0.5)
    momentum = features.get('momentum_score', 0)
    
    # Skip if RSI is extreme but trend is weak (potential reversal trap)
    if (rsi > 70 or rsi < 30) and trend_strength < 0.4:
        return "skip"
    
    # Skip if price at extreme Bollinger position without momentum confirmation
    if (bb_position < 0.1 or bb_position > 0.9) and momentum < 0.3:
        return "skip"
    
    return prediction