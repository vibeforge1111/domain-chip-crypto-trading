def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions with confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == "long" and bb_pct_b < 0.05:
        if stoch_k < 20 and rsi_2h > 30 and obv_slope > 0:
            return prediction
    
    if prediction == "short" and bb_pct_b > 0.95:
        if stoch_k > 80 and rsi_2h < 70 and obv_slope < 0:
            return prediction
    
    return "skip"