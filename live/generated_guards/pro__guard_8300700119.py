def guard(features: dict, prediction: str) -> str:
    """Filter trades with conflicting momentum and candle structure signals."""
    
    # Reject long if RSI overbought and candle shows reversal candle (upper wick)
    if prediction == "long" and features['rsi_14'] > 68:
        if features['upper_wick_ratio'] > 0.25:
            return "skip"
    
    # Reject short if RSI oversold and candle shows reversal candle (lower wick)
    if prediction == "short" and features['rsi_14'] < 32:
        if features['lower_wick_ratio'] > 0.25:
            return "skip"
    
    # Reject trades with low body + low volume (no conviction)
    if features['body_ratio'] < 0.15 and features['volume_ratio'] < 0.7:
        return "skip"
    
    return prediction