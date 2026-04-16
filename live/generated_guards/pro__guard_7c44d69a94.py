def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == "long":
        # Skip long when both indicators show overbought extremes (reversal risk)
        if bb_pct_b > 0.8 and stoch_k > 80:
            return "skip"
    elif prediction == "short":
        # Skip short when both indicators show oversold extremes (reversal risk)
        if bb_pct_b < 0.2 and stoch_k < 20:
            return "skip"
    
    return prediction