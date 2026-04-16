def guard(features: dict, prediction: str) -> str:
    # True compression: low ATR + tight BB → allow if momentum aligned
    if features['atr_ratio'] < 0.7 and features['bb_width'] < 0.15:
        # Check momentum alignment with prediction
        if prediction == "long" and features['macd_histogram'] < 0:
            return "skip"
        if prediction == "short" and features['macd_histogram'] > 0:
            return "skip"
        return prediction
    # False compression: low ATR but wide BB (fake squeeze) → skip
    if features['atr_ratio'] < 0.7 and features['bb_width'] > 0.22:
        return "skip"
    # Check for extreme stoch position during compression
    if features['bb_width'] < 0.12 and (features['stoch_k'] < 15 or features['stoch_k'] > 85):
        if features['rsi_2h'] > 65 or features['rsi_2h'] < 35:
            return "skip"
    return prediction