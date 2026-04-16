def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == "long":
        if bb_pct_b >= 0.05:
            return "skip"
        if rsi_2h > 70:
            return "skip"
    elif prediction == "short":
        if bb_pct_b <= 0.95:
            return "skip"
        if rsi_2h < 30:
            return "skip"
    
    return prediction