def guard(features: dict, prediction: str) -> str:
    # Reject if candle has excessive wicks (unclear market structure)
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    if total_wick > 0.75:
        return "skip"
    
    # Reject if RSI extreme without momentum/trend alignment
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    if (rsi > 70 or rsi < 30) and momentum * (1 if prediction == "long" else -1) < 0:
        return "skip"
    
    # Reject if low volume during breakout-like moves
    if features.get('volume_ratio', 1) < 0.6 and features.get('range_pct', 0) > 0.02:
        return "skip"
    
    return prediction