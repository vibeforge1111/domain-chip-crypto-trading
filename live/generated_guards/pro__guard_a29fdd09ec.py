def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # High-confidence entry: extreme bb position (<0.05 or >0.95)
    in_extreme_bb = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    # Stochastic confirmation: oversold for longs, overbought for shorts
    if prediction == "long":
        stoch_confirm = stoch_k < 25
    else:
        stoch_confirm = stoch_k > 75
    
    if in_extreme_bb and stoch_confirm:
        return prediction
    
    return "skip"