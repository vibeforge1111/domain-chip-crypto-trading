def guard(features: dict, prediction: str) -> str:
    """Filter trades with extreme Bollinger position but weak trend confirmation."""
    if features['bb_position'] > 0.9 and features['trend_strength'] < 0.4:
        return "skip"
    if features['bb_position'] < 0.1 and features['trend_strength'] < 0.4:
        return "skip"
    return prediction