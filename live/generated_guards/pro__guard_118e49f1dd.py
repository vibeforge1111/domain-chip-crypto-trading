def guard(features: dict, prediction: str) -> str:
    # Filter longs when overbought: stoch_k > 80 and bb_pct_b > 0.85
    if prediction == "long" and features.get("stoch_k", 0) > 80 and features.get("bb_pct_b", 0) > 0.85:
        return "skip"
    
    # Filter shorts when oversold: stoch_k < 20 and bb_pct_b < 0.15
    if prediction == "short" and features.get("stoch_k", 0) < 20 and features.get("bb_pct_b", 0) < 0.15:
        return "skip"
    
    return prediction