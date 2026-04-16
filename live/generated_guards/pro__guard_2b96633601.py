def guard(features: dict, prediction: str) -> str:
    """Guard focusing on wick dominance and momentum confirmation."""
    # Skip if wicks dominate the candle (weak directional signal)
    if features['upper_wick_ratio'] > 0.45 or features['lower_wick_ratio'] > 0.45:
        if features['body_ratio'] < 0.3:
            return "skip"
    
    # Filter extreme RSI without momentum alignment
    if features['rsi_14'] > 72 and features['momentum_score'] < 0.3:
        return "skip"
    if features['rsi_14'] < 28 and features['momentum_score'] > -0.3:
        return "skip"
    
    # Skip low volatility compression unless trend is strong
    if features['bb_width'] < 0.6 and features['trend_strength'] < 0.4:
        return "skip"
    
    return prediction