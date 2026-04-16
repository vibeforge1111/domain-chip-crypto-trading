def guard(features: dict, prediction: str) -> str:
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip trades against volume flow direction (primary filter)
    if prediction == "long" and obv_slope < -0.001:
        return "skip"
    if prediction == "short" and obv_slope > 0.001:
        return "skip"
    
    # Additional confirmation with stochastic alignment
    if prediction == "long" and stoch_k < 20 and stoch_d < 20:
        return "skip"
    if prediction == "short" and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    return prediction