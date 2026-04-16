def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak candle structure, low volume, or unconfirmed momentum."""
    # Reject if candle has excessive wicks relative to body (weak structure)
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 1)
    if total_wick > body_ratio * 1.5:
        return "skip"
    
    # Reject if volume is too low (lack of conviction)
    if features.get('volume_ratio', 1) < 0.5:
        return "skip"
    
    # Reject if RSI in extreme territory without strong momentum confirmation
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    if (rsi > 70 or rsi < 30) and abs(momentum) < 0.3:
        return "skip"
    
    return prediction