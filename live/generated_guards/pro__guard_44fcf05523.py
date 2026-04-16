def guard(features: dict, prediction: str) -> str:
    """Filter trades based on volume-momentum divergence and extreme RSI with candle confirmation."""
    if features.get('volume_ratio', 1) < 0.7 and features.get('momentum_score', 0) < 0.3:
        return "skip"
    
    if features.get('rsi_14', 50) > 75 and features.get('upper_wick_ratio', 0) > 0.4 and prediction == "long":
        return "skip"
    
    if features.get('rsi_14', 50) < 25 and features.get('lower_wick_ratio', 0) > 0.4 and prediction == "short":
        return "skip"
    
    if features.get('bb_width', 0) < 0.3 and features.get('volume_ratio', 1) > 1.8 and features.get('range_pct', 0) < 0.5:
        return "skip"
    
    return prediction