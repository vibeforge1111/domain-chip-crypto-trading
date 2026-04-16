def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # High-confidence entries only at BB extremes with multi-confirmation
    if prediction == "long" and bb_pct_b < 0.05 and stoch_k < 25 and rsi_2h < 40 and vwap_dev < 0:
        return prediction
    if prediction == "short" and bb_pct_b > 0.95 and stoch_k > 75 and rsi_2h > 60 and vwap_dev > 0:
        return prediction
    
    return "skip"