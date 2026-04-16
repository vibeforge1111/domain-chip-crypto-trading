def guard(features: dict, prediction: str) -> str:
    # Filter weak signals: small body with high volume and volatility often indicates rejection/whipsaw
    if (features['body_ratio'] < 0.25 and 
        features['volume_ratio'] > 1.4 and 
        features['volatility_regime'] > 0.65):
        return "skip"
    return prediction