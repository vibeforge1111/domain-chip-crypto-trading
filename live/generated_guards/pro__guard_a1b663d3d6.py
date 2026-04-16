def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Long: bb_pct_b < 0.05 (near lower band = oversold zone)
    if prediction == "long":
        if bb_pct >= 0.05:
            return "skip"
        if stoch_k > 30:
            return "skip"
    
    # Short: bb_pct_b > 0.95 (near upper band = overbought zone)
    if prediction == "short":
        if bb_pct <= 0.95:
            return "skip"
        if stoch_k < 70:
            return "skip"
    
    return prediction