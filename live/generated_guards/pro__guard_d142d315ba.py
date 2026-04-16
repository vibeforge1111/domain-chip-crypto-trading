def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # Long only when near lower band with confirmation
    if bb_pct_b < 0.05 and prediction == "long":
        if vwap_dev < -0.005 and stoch_k < 20 and obv_slope > 0:
            return prediction
        return "skip"
    # Short only when near upper band with confirmation
    elif bb_pct_b > 0.95 and prediction == "short":
        if vwap_dev > 0.005 and stoch_k > 80 and obv_slope < 0:
            return prediction
        return "skip"
    return prediction