def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones with confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    # Long entry: bb_pct_b < 0.05 and stochastic confirmation (both below 20)
    if prediction == "long":
        if bb_pct_b >= 0.05 or stoch_k <= 20 or stoch_d <= 20:
            return "skip"
        if volume_ratio < 0.7:
            return "skip"
    
    # Short entry: bb_pct_b > 0.95 and stochastic confirmation (both above 80)
    if prediction == "short":
        if bb_pct_b <= 0.95 or stoch_k >= 80 or stoch_d >= 80:
            return "skip"
        if volume_ratio < 0.7:
            return "skip"
    
    return prediction