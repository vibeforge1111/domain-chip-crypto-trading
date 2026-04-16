def guard(features: dict, prediction: str) -> str:
    stoch_diff = features.get('stoch_k', 50) - features.get('stoch_d', 50)
    bb_pos = features.get('bb_pct_b', 0.5)
    
    if prediction == "long" and stoch_diff < 0:
        return "skip"
    if prediction == "short" and stoch_diff > 0:
        return "skip"
    
    if prediction == "long" and bb_pos > 0.9:
        return "skip"
    if prediction == "short" and bb_pos < 0.1:
        return "skip"
    
    return prediction