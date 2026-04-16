def guard(features: dict, prediction: str) -> str:
    """Filter trades with high volatility but weak volume confirmation."""
    if features['atr_ratio'] > 1.5 and features['volume_ratio'] < 0.7:
        return "skip"
    return prediction