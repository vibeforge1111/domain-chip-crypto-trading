def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using BB width and ATR expansion."""
    if features['bb_width'] < 0.12:
        if features['atr_ratio'] > 1.4 and features['volume_ratio'] < 0.8:
            return "skip"
    return prediction