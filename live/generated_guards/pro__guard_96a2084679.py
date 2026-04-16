def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum and trend direction are misaligned."""
    momentum = features.get('momentum_score', 0)
    ema_slope = features.get('ema_slope', 0)
    rsi = features.get('rsi_14', 50)
    
    # For long trades, require positive momentum and uptrend
    if prediction == "long":
        if momentum < 0 or ema_slope < 0:
            return "skip"
        # Avoid extreme overbought levels for longs
        if rsi > 78:
            return "skip"
    
    # For short trades, require negative momentum and downtrend
    elif prediction == "short":
        if momentum > 0 or ema_slope > 0:
            return "skip"
        # Avoid extreme oversold levels for shorts
        if rsi < 22:
            return "skip"
    
    return prediction