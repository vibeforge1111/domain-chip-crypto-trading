def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    if bb_pct_b < 0.05 and stoch_k < 20 and stoch_d < 20 and rsi_2h < 60:
        return prediction
    if bb_pct_b > 0.95 and stoch_k > 80 and stoch_d > 80 and rsi_2h > 40:
        return prediction
    
    return "skip"