def guard(features: dict, prediction: str) -> str:
    """Filter trades based on candle structure alignment with direction and momentum."""
    # Check RSI zones for trade validity
    rsi = features.get("rsi_14", 50)
    
    # For long signals: require RSI oversold (<35) or at least neutral
    if prediction == "long" and rsi > 65:
        return "skip"
    
    # For short signals: require RSI overbought (>65) or at least neutral
    if prediction == "short" and rsi < 35:
        return "skip"
    
    # Align wick direction with prediction (bullish candle for longs, bearish for shorts)
    if prediction == "long" and features.get("upper_wick_ratio", 0) > features.get("lower_wick_ratio", 0) * 1.5:
        return "skip"
    
    if prediction == "short" and features.get("lower_wick_ratio", 0) > features.get("upper_wick_ratio", 0) * 1.5:
        return "skip"
    
    # Require solid body (not doji/indecision candles)
    if features.get("body_ratio", 1) < 0.25:
        return "skip"
    
    return prediction