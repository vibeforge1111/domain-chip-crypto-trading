def guard(features: dict, prediction: str) -> str:
    """Reject trades in high-volatility chop with weak momentum."""
    if features['volatility_regime'] > 0.65 and features['momentum_score'] < 0.3:
        return "skip"
    return prediction