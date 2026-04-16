def guard(features: dict, prediction: str) -> str:
    """Filter signals based on volatility expansion and RSI-candle divergence."""
    # Skip if high volume but narrow BBs (potential liquidity grab)
    if features['volume_ratio'] > 1.8 and features['bb_width'] < 0.35:
        return "skip"
    
    # Skip long when RSI overbought with large upper wick (weak rejection)
    if prediction == "long" and features['rsi_14'] > 68 and features['upper_wick_ratio'] > 0.25:
        return "skip"
    
    # Skip short when RSI oversold with large lower wick
    if prediction == "short" and features['rsi_14'] < 32 and features['lower_wick_ratio'] > 0.25:
        return "skip"
    
    return prediction