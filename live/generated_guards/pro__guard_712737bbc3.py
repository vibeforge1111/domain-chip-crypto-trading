def guard(features: dict, prediction: str) -> str:
    """Reject trades with RSI/EMA divergence or extreme BB position."""
    rsi_14 = features.get('rsi_14', 50)
    ema_slope = features.get('ema_slope', 0)
    bb_position = features.get('bb_position', 0.5)
    volume_ratio = features.get('volume_ratio', 1)
    
    # In uptrend, reject overbought RSI with weak EMA slope
    if prediction == "long" and rsi_14 > 70 and ema_slope < 0.1:
        return "skip"
    
    # In downtrend, reject oversold RSI with positive EMA slope  
    if prediction == "short" and rsi_14 < 30 and ema_slope > -0.1:
        return "skip"
    
    # Reject entries at extreme BB edges with high volume (exhaustion risk)
    if volume_ratio > 1.5 and (bb_position < 0.05 or bb_position > 0.95):
        return "skip"
    
    return prediction