def guard(features: dict, prediction: str) -> str:
    # Skip if momentum is strong but volume is weak (potential false signal)
    if abs(features['momentum_score']) > 0.6 and features['volume_ratio'] < 0.7:
        return "skip"
    return prediction