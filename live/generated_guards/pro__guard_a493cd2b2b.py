def guard(features: dict, prediction: str) -> str:
    # Skip if high volume but small range - potential manipulation or fakeout
    if features.get('volume_ratio', 1) > 2.0 and features.get('range_pct', 0.5) < 0.5:
        return "skip"
    
    # Skip long signals when RSI oversold but EMA still declining
    if prediction == "long" and features.get('rsi_14', 50) < 40 and features.get('ema_slope', 0) < 0:
        return "skip"
    
    # Skip short signals when RSI overbought but EMA still rising
    if prediction == "short" and features.get('rsi_14', 50) > 60 and features.get('ema_slope', 0) > 0:
        return "skip"
    
    return prediction