def guard(features: dict, prediction: str) -> str:
    """Skip trades when low volume coincides with high ATR (choppy market)."""
    # Low volume + high volatility = unreliable signals
    if features['volume_ratio'] < 0.6 and features['atr_ratio'] > 1.4:
        return "skip"
    return prediction