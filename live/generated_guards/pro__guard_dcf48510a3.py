def guard(features: dict, prediction: str) -> str:
    # Low conviction filter: reject weak signals with low volume AND small range
    if features.get('volume_ratio', 1) < 0.6 and features.get('range_pct', 1) < 0.4:
        return "skip"
    
    # Momentum-trend divergence filter: reject when momentum contradicts trend direction
    momentum = features.get('momentum_score', 0)
    trend = features.get('trend_strength', 0)
    
    if prediction == "long":
        # For longs, momentum should not be strongly negative against trend
        if momentum < -0.2 and trend > 0:
            return "skip"
    elif prediction == "short":
        # For shorts, momentum should not be strongly positive against trend
        if momentum > 0.2 and trend < 0:
            return "skip"
    
    return prediction