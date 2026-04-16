def guard(features: dict, prediction: str) -> str:
    """Skip trades in choppy/volatile conditions with weak trend."""
    if features['atr_ratio'] > 1.3 and features['trend_strength'] < 0.4 and features['volume_ratio'] > 1.5:
        return "skip"
    return prediction