def guard(features: dict, prediction: str) -> str:
    """Filter trades based on candle structure quality and momentum alignment."""
    # Extract wick and body metrics
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 0)
    ema_slope = features.get('ema_slope', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Large wicks indicate rejection/reversal - filter these
    total_wick = upper_wick + lower_wick
    if total_wick > 0.7:
        return "skip"
    
    # Small body in large wick candle = indecision
    if body_ratio < 0.2 and total_wick > 0.5:
        return "skip"
    
    # Momentum-trend divergence weakens signal
    if ema_slope > 0 and momentum_score < -0.3:
        return "skip"
    if ema_slope < 0 and momentum_score > 0.3:
        return "skip"
    
    return prediction