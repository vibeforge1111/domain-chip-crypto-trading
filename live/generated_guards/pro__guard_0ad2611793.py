def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct = features.get("bb_pct_b", 0.5)
    rsi = features.get("rsi_14", 50)
    
    # Skip if too close to VWAP (within 0.3%) and middle of Bollinger Band
    if abs(vwap_dev) < 0.003 and 0.35 < bb_pct < 0.65 and 45 < rsi < 55:
        return "skip"
    
    return prediction