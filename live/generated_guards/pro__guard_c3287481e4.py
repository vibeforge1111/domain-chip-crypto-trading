def guard(features: dict, prediction: str) -> str:
    # Reject trades where volume is high but momentum is weak (potential reversal signal)
    if features['volume_ratio'] > 1.5 and features['momentum_score'] < 0.3:
        return "skip"
    return prediction