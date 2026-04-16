def guard(features: dict, prediction: str) -> str:
    """Reject high-volume exhaustion candles at extreme BB positions."""
    if features['volume_ratio'] > 1.8 and (features['bb_position'] > 0.92 or features['bb_position'] < 0.08):
        return "skip"
    return prediction