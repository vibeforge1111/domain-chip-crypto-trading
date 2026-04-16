def guard(features: dict, prediction: str) -> str:
    # Reject signals where momentum diverges from volume confirmation
    if features['volume_ratio'] > 1.4 and features['momentum_score'] < 0 and prediction == "long":
        return "skip"
    if features['volume_ratio'] > 1.4 and features['momentum_score'] > 0 and prediction == "short":
        return "skip"
    return prediction