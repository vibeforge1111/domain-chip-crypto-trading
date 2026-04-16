def guard(features: dict, prediction: str) -> str:
    """Filter trades with RSI-trend divergence or Bollinger squeeze without momentum."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    ema_slope = features.get("ema_slope", 0)
    momentum = features.get("momentum_score", 0)
    bb_width = features.get("bb_width", 0.1)
    
    # Filter: RSI overbought but price still falling (for longs), or vice versa
    if rsi > 65 and ema_slope < 0 and prediction == "long":
        return "skip"
    if rsi < 35 and ema_slope > 0 and prediction == "short":
        return "skip"
    
    # Filter: Bollinger squeeze (low bb_width) without momentum confirmation
    if bb_width < 0.05 and abs(momentum) < 0.2:
        return "skip"
    
    return prediction