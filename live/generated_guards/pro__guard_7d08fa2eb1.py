def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    if prediction == "long":
        if bb_pct > 0.90 and stoch_k > 80:
            return "skip"
        if vwap_dev > 0.03:
            return "skip"
    
    if prediction == "short":
        if bb_pct < 0.10 and stoch_k < 20:
            return "skip"
        if vwap_dev < -0.03:
            return "skip"
    
    return prediction