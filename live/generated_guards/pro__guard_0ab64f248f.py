def guard(features: dict, prediction: str) -> str:
    """Reject trades with momentum/trend divergence."""
    # Skip long if downtrend but momentum positive
    if prediction == "long" and features['trend_strength'] < -0.3 and features['momentum_score'] > 0.2:
        return "skip"
    # Skip short if uptrend but momentum negative
    if prediction == "short" and features['trend_strength'] > 0.3 and features['momentum_score'] < -0.2:
        return "skip"
    return prediction