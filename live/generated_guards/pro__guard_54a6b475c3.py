def guard(features: dict, prediction: str) -> str:
    # Skip if body is small relative to range (whipsaw prone)
    if features['body_ratio'] < 0.25:
        return "skip"
    
    # Skip if volume is too low (weak conviction)
    if features['volume_ratio'] < 0.5:
        return "skip"
    
    return prediction