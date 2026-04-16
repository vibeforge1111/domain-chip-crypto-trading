def guard(features: dict, prediction: str) -> str:
    # Skip momentum divergence: RSI overbought in uptrend or oversold in downtrend
    if prediction == "long" and features.get("rsi_14", 50) > 68 and features.get("ema_slope", 0) > 0:
        return "skip"
    if prediction == "short" and features.get("rsi_14", 50) < 32 and features.get("ema_slope", 0) < 0:
        return "skip"
    
    # Skip reversal wicks: large upper wick on long signal or lower wick on short signal
    if prediction == "long" and features.get("upper_wick_ratio", 0) > 0.5:
        return "skip"
    if prediction == "short" and features.get("lower_wick_ratio", 0) > 0.5:
        return "skip"
    
    return prediction