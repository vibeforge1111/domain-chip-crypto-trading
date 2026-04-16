def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # High-confidence entry zones at Bollinger Band extremes
    # Lower extreme (<0.05) for longs, upper extreme (>0.95) for shorts
    if bb_pct_b < 0.05 and prediction == "long":
        return prediction
    if bb_pct_b > 0.95 and prediction == "short":
        return prediction
    
    return "skip"