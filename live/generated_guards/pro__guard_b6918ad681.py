def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Only allow entries at extreme BB positions with stoch confirmation
    # Long: bb_pct_b < 0.05 AND stoch oversold (<20)
    # Short: bb_pct_b > 0.95 AND stoch overbought (>80)
    if prediction == "long":
        if bb_pct_b >= 0.05 or stoch_k >= 20:
            return "skip"
    elif prediction == "short":
        if bb_pct_b <= 0.95 or stoch_k <= 80:
            return "skip"
    
    return prediction