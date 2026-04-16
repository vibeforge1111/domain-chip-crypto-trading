def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum contradicts trend strength."""
    # Weak momentum in weak trend = low conviction
    if features['momentum_score'] < 0.25 and features['trend_strength'] < 0.35:
        return "skip"
    # Strong momentum in strong trend = likely exhausted
    if features['momentum_score'] > 0.85 and features['trend_strength'] > 0.75:
        return "skip"
    return prediction