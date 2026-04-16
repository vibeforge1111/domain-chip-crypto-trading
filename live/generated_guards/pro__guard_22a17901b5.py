def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Long only when bb_pct_b < 0.05 (at lower band) AND stoch_k < 20 (oversold)
    if prediction == "long":
        if not (bb_pct_b < 0.05 and stoch_k < 20):
            return "skip"
    
    # Short only when bb_pct_b > 0.95 (at upper band) AND stoch_k > 80 (overbought)
    elif prediction == "short":
        if not (bb_pct_b > 0.95 and stoch_k > 80):
            return "skip"
    
    return prediction