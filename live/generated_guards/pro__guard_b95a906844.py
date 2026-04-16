def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # High-confidence entry zones: BB extreme + stoch confirmation + volume flow
    if prediction == "long" and bb_pct < 0.05 and stoch_k < 25 and obv_slope > 0:
        return prediction
    if prediction == "short" and bb_pct > 0.95 and stoch_k > 75 and obv_slope < 0:
        return prediction
    
    return "skip"