def guard(features: dict, prediction: str) -> str:
    """Reject trades when candle structure is unreliable or momentum contradicts signal."""
    body_ratio = features.get("body_ratio", 0.5)
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    rsi = features.get("rsi_14", 50)
    bb_position = features.get("bb_position", 0.5)
    momentum = features.get("momentum_score", 0)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Doji-like candle: small body, dominant wick - unreliable signal
    if body_ratio < 0.25 and max(upper_wick, lower_wick) > 0.5:
        return "skip"
    
    # Extreme RSI in wrong direction for the prediction
    if prediction == "long" and rsi > 75:
        return "skip"
    if prediction == "short" and rsi < 25:
        return "skip"
    
    # BB extreme with weak momentum - potential reversal trap
    if bb_position > 0.9 and momentum < 0:
        return "skip"
    if bb_position < 0.1 and momentum > 0:
        return "skip"
    
    # High volume + narrow range + extreme BB = exhaustion move
    if volume_ratio > 2 and features.get("range_pct", 0) < 0.3:
        if bb_position < 0.15 or bb_position > 0.85:
            return "skip"
    
    return prediction