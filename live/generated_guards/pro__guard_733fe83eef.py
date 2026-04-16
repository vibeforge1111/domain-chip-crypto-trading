def guard(features: dict, prediction: str) -> str:
    """Reject trades with poor candle structure and weak momentum alignment."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 0)
    bb_position = features.get('bb_position', 0.5)
    ema_slope = features.get('ema_slope', 0)
    trend_strength = features.get('trend_strength', 0)
    
    # Reject if candle has excessive wicks (poor structure)
    if upper_wick + lower_wick > 0.7:
        return "skip"
    
    # Reject if body is too small relative to wicks
    if body_ratio < 0.2:
        return "skip"
    
    # Reject counter-trend trades at Bollinger extremes
    if prediction == 'long' and bb_position > 0.85 and ema_slope < 0:
        return "skip"
    if prediction == 'short' and bb_position < 0.15 and ema_slope > 0:
        return "skip"
    
    # Reject if weak trend + weak BB signal
    if trend_strength < 0.25 and (bb_position > 0.8 or bb_position < 0.2):
        return "skip"
    
    return prediction