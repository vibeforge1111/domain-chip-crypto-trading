def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    volume_ratio = features.get('volume_ratio', 1)
    
    if prediction == "long":
        if bb_pct_b < 0.05 and vwap_deviation < 0 and rsi_2h < 70 and volume_ratio >= 0.8:
            return prediction
        return "skip"
    elif prediction == "short":
        if bb_pct_b > 0.95 and vwap_deviation > 0 and rsi_2h > 30 and volume_ratio >= 0.8:
            return prediction
        return "skip"
    
    return prediction