def guard(features: dict, prediction: str) -> str:
    # Detect momentum deceleration before entry
    macd_hist = features.get('macd_histogram', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long entries when momentum is decelerating in overbought context
    if prediction == "long" and macd_hist < -0.0005 and rsi_2h > 65:
        return "skip"
    
    # Skip short entries when momentum is decelerating in oversold context
    if prediction == "short" and macd_hist > 0.0005 and rsi_2h < 35:
        return "skip"
    
    return prediction