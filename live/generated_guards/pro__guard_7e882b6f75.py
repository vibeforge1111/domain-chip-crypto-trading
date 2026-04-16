def guard(features: dict, prediction: str) -> str:
    """Filter trades against volume flow direction using obv_slope."""
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when volume flow is bearish (distribution)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip shorts when volume flow is bullish (accumulation)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    # Additional filter: avoid longs in overbought conditions
    if prediction == "long" and stoch_k > 80:
        return "skip"
    
    return prediction