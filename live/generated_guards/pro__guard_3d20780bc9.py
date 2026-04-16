def guard(features: dict, prediction: str) -> str:
    # Filter low-range candles (chop/noise)
    if features['range_pct'] < 0.005:
        return "skip"
    
    # Skip long when downtrend + overbought RSI (momentum divergence)
    if prediction == "long":
        if features['ema_slope'] < 0 and features['rsi_14'] > 55:
            return "skip"
    
    # Skip short when uptrend + oversold RSI (momentum divergence)
    if prediction == "short":
        if features['ema_slope'] > 0 and features['rsi_14'] < 45:
            return "skip"
    
    # Require minimum volume to confirm institutional interest
    if features['volume_ratio'] < 0.7:
        return "skip"
    
    return prediction