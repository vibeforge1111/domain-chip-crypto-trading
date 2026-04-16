def guard(features: dict, prediction: str) -> str:
    # Detect false compression: low BB width but rising ATR = likely breakout
    if features['bb_width'] < 0.12 and features['atr_ratio'] > 1.3:
        return "skip"
    
    # Skip overbought/oversold extremes conflicting with direction
    if features['stoch_k'] > 88 and prediction == "long":
        return "skip"
    if features['stoch_k'] < 12 and prediction == "short":
        return "skip"
    
    # Filter if too far from VWAP (reversion risk)
    if features['vwap_deviation'] > 0.025 and prediction == "long":
        return "skip"
    if features['vwap_deviation'] < -0.025 and prediction == "short":
        return "skip"
    
    return prediction