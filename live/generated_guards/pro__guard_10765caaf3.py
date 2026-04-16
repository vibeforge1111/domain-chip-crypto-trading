def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == "long":
        if bb_pct_b < 0.05 and stoch_k < 30 and obv_slope > 0:
            return prediction
    elif prediction == "short":
        if bb_pct_b > 0.95 and stoch_k > 70 and obv_slope < 0:
            return prediction
    
    return "skip"