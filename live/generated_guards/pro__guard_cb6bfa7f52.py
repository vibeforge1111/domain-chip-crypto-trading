def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum contradicts trend direction."""
    # Skip when strong trend but weak/bearish momentum
    if features['trend_strength'] > 0.7 and features['momentum_score'] < 0:
        return "skip"
    # Skip when weak trend but strong momentum (low conviction)
    if features['trend_strength'] < 0.4 and features['momentum_score'] > 0.5:
        return "skip"
    return prediction