def guard(features: dict, prediction: str) -> str:
    # Skip when momentum diverges from candle strength (weak body with strong momentum)
    if features['momentum_score'] > 65 and features['body_ratio'] < 0.25:
        return "skip"
    if features['momentum_score'] < 35 and features['body_ratio'] < 0.25:
        return "skip"
    return prediction