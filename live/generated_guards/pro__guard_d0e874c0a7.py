def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak conviction near VWAP and misaligned momentum."""
    # Skip if price too close to VWAP (indecision zone)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    
    # Skip longs when overbought or negative momentum
    if prediction == "long":
        if features.get('stoch_k', 50) > 80:
            return "skip"
        if features.get('macd_histogram', 0) < -0.0001:
            return "skip"
    
    # Skip shorts when oversold or positive momentum
    if prediction == "short":
        if features.get('stoch_k', 50) < 20:
            return "skip"
        if features.get('macd_histogram', 0) > 0.0001:
            return "skip"
    
    return prediction