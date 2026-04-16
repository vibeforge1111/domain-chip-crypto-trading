def guard(features: dict, prediction: str) -> str:
    """Custom guard function using BB extremes and momentum confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    if prediction == "long":
        # High-confidence long: extreme lower band OR pullback with momentum
        if bb_pct_b < 0.05 or (bb_pct_b < 0.15 and stoch_k < 25 and volume_ratio > 0.8):
            return prediction
        return "skip"
    
    elif prediction == "short":
        # High-confidence short: extreme upper band OR rally with momentum
        if bb_pct_b > 0.95 or (bb_pct_b > 0.85 and stoch_k > 75 and volume_ratio > 0.8):
            return prediction
        return "skip"
    
    return prediction