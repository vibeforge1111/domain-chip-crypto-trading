def guard(features: dict, prediction: str) -> str:
    """Filter trades based on candle rejection patterns and momentum divergence."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    body_ratio = features.get("body_ratio", 1)
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    
    if prediction == "long":
        # Reject if candle shows rejection from above (large upper wick)
        if upper_wick > 0.45 and body_ratio < 0.35:
            return "skip"
        # Reject if overbought AND momentum diverging from price
        if rsi > 72 and momentum < 0:
            return "skip"
    
    if prediction == "short":
        # Reject if candle shows rejection from below (large lower wick)
        if lower_wick > 0.45 and body_ratio < 0.35:
            return "skip"
        # Reject if oversold AND momentum diverging from price
        if rsi < 28 and momentum > 0:
            return "skip"
    
    return prediction