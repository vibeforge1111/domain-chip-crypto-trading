def guard(features: dict, prediction: str) -> str:
    """Filter trades on momentum deceleration using macd_histogram."""
    # Skip if macd_histogram shows strong negative momentum (deceleration)
    if features['macd_histogram'] < -0.0004:
        return "skip"
    # Skip if negative macd combined with overbought stoch (divergence signal)
    if features['macd_histogram'] < 0 and features['stoch_k'] > 75:
        return "skip"
    return prediction