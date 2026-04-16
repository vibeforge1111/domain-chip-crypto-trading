def guard(features: dict, prediction: str) -> str:
    # Filter out longs when momentum contradicts BB upper position
    if prediction == "long" and features['momentum_score'] < -0.3 and features['bb_position'] > 0.85:
        return "skip"
    # Filter out shorts when momentum contradicts BB lower position
    if prediction == "short" and features['momentum_score'] > 0.3 and features['bb_position'] < 0.15:
        return "skip"
    return prediction