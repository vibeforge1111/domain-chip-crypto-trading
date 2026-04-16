def guard(features: dict, prediction: str) -> str:
    """Reject trades with weak candle conviction and momentum divergence."""
    body_ratio = features.get('body_ratio', 0)
    upper_wick_ratio = features.get('upper_wick_ratio', 0)
    lower_wick_ratio = features.get('lower_wick_ratio', 0)
    trend_strength = features.get('trend_strength', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Reject if candle has weak conviction (small body, large wicks)
    if body_ratio < 0.25 and (upper_wick_ratio + lower_wick_ratio) > 0.5:
        return "skip"
    
    # Reject if trend strength and momentum are diverging
    if trend_strength * momentum_score < 0:
        return "skip"
    
    return prediction