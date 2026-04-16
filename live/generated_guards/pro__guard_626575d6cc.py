def guard(features: dict, prediction: str) -> str:
    """Filter trades with conflicting momentum and Bollinger Band position."""
    if features['bb_position'] > 0.9 and features['momentum_score'] < -0.2:
        return "skip"
    if features['bb_position'] < 0.1 and features['momentum_score'] > 0.2:
        return "skip"
    return prediction