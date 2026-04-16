def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # High-confidence entries only at BB extremes
    at_lower_extreme = bb_pct < 0.05
    at_upper_extreme = bb_pct > 0.95
    
    # Validate longs at lower band with oversold confirmation
    if prediction == "long" and at_lower_extreme and stoch_k < 25:
        return prediction
    
    # Validate shorts at upper band with overbought confirmation
    if prediction == "short" and at_upper_extreme and stoch_k > 75:
        return prediction
    
    return "skip"