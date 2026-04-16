def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get("bb_pct_b", 0.5)
    rsi = features.get("rsi_14", 50)
    stoch = features.get("stoch_k", 50)
    
    # High-confidence entry zones: bb_pct_b at extremes with momentum confirmation
    if bb_pct < 0.05 and prediction == "long" and rsi > 25 and stoch < 85:
        return prediction
    if bb_pct > 0.95 and prediction == "short" and rsi < 75 and stoch > 15:
        return prediction
    
    return "skip"