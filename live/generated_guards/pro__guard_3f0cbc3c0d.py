def guard(features: dict, prediction: str) -> str:
    # Reject longs when overbought (bb_pct_b high AND stoch_k high)
    if prediction == "long":
        if features.get("bb_pct_b", 0.5) > 0.85 and features.get("stoch_k", 50) > 80:
            return "skip"
    
    # Reject shorts when oversold (bb_pct_b low AND stoch_k low)
    if prediction == "short":
        if features.get("bb_pct_b", 0.5) < 0.15 and features.get("stoch_k", 50) < 20:
            return "skip"
    
    return prediction