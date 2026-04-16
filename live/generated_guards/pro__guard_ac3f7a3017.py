def guard(features: dict, prediction: str) -> str:
    """Reject signals on weak candles in high-vol environments with poor volume."""
    if features['body_ratio'] < 0.25:
        return "skip"
    if features['volatility_regime'] > 1.5 and features['volume_ratio'] < 0.8:
        return "skip"
    if features['bb_position'] > 0.9 or features['bb_position'] < 0.1:
        return "skip"
    return prediction