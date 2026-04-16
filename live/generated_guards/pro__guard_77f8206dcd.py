def guard(features: dict, prediction: str) -> str:
    """Filter trades on doji patterns, BB squeeze without momentum, or RSI/EMA divergence."""
    body_ratio = features.get("body_ratio", 0.5)
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    bb_width = features.get("bb_width", 0.02)
    momentum = features.get("momentum_score", 0)
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    
    # Doji/pin bar: small body, large wicks
    if body_ratio < 0.15 and (upper_wick + lower_wick) > 0.7:
        return "skip"
    
    # BB squeeze without momentum confirmation
    if bb_width < 0.015 and abs(momentum) < 0.3:
        return "skip"
    
    # RSI/EMA divergence: RSI extreme in opposite direction of trend
    if rsi > 70 and ema_slope < 0:
        return "skip"
    if rsi < 30 and ema_slope > 0:
        return "skip"
    
    return prediction