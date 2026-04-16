def guard(features: dict, prediction: str) -> str:
    # Reject low-quality candles (small body relative to total range)
    if features['body_ratio'] < 0.35:
        return "skip"
    
    # Require trend alignment between EMA slope and momentum score
    if features['ema_slope'] * features['momentum_score'] < 0:
        return "skip"
    
    # For long signals: positive momentum required + RSI not overbought
    if prediction == "long":
        if features['momentum_score'] < 0.15 or features['rsi_14'] > 75:
            return "skip"
    
    # For short signals: negative momentum required + RSI not oversold
    elif prediction == "short":
        if features['momentum_score'] > -0.15 or features['rsi_14'] < 25:
            return "skip"
    
    # Avoid low volatility chop (BB squeeze filter)
    if features['bb_width'] < 0.5:
        return "skip"
    
    return prediction