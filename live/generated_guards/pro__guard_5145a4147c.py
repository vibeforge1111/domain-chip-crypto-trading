def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get('bb_pct_b', 0.5)
    vwap = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    stoch_2h = features.get('stoch_k', 50)
    
    if bb_pct < 0.05:
        if vwap < -0.002 and stoch > 20 and stoch_2h > 30:
            return prediction
    elif bb_pct > 0.95:
        if vwap > 0.002 and stoch < 80 and stoch_2h < 70:
            return prediction
    
    return "skip"