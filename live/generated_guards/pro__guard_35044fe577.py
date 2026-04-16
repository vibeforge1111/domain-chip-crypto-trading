def guard(features: dict, prediction: str) -> str:
    """Filter trades during compression breakouts (low ATR + high volume = often fail)."""
    if features['atr_ratio'] < 0.5 and features['volume_ratio'] > 1.5:
        return "skip"
    return prediction