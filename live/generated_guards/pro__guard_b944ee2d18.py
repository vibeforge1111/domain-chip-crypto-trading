def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    # High-confidence entries: extreme BB position + aligned RSI context
    if prediction == "long":
        if bb_pct_b < 0.05 and rsi_2h > 35:
            return prediction
    elif prediction == "short":
        if bb_pct_b > 0.95 and rsi_2h < 65:
            return prediction
    
    return "skip"