def guard(features: dict, prediction: str) -> str:
    """Reject signals with high volatility but weak momentum alignment."""
    if features['volatility_regime'] > 1.5 and features['momentum_score'] < 0.3:
        return "skip"
    return prediction