def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum-price divergence."""
    if features['rsi_14'] > 70 and features['momentum_score'] < 0.3:
        return "skip"
    if features['rsi_14'] < 30 and features['momentum_score'] > 0.7:
        return "skip"
    return prediction