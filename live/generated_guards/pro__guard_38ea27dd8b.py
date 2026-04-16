def guard(features: dict, prediction: str) -> str:
    # True squeeze: low atr_ratio AND low bb_width = compression
    is_true_squeeze = features.get('atr_ratio', 1) < 1.0 and features.get('bb_width', 1) < 0.9
    
    # False compression: high volatility but tight bands = likely rejection
    if features.get('atr_ratio', 1) > 1.5 and features.get('bb_width', 1) < 1.1:
        return "skip"
    
    # Skip extreme stochastic readings
    if features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15:
        return "skip"
    
    # Skip if 2h RSI conflicts with prediction direction
    rsi_2h = features.get('rsi_2h', 50)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction