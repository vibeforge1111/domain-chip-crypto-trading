def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Both indicators show overbought - reject long signals
    if bb_pct_b > 0.9 and stoch_k > 80 and prediction == "long":
        return "skip"
    
    # Both indicators show oversold - reject short signals
    if bb_pct_b < 0.1 and stoch_k < 20 and prediction == "short":
        return "skip"
    
    return prediction