def guard(features: dict, prediction: str) -> str:
    # Filter: skip if volatility is compressed AND price at extreme BB position
    if features['bb_width'] < 0.012 and (features['bb_position'] > 0.92 or features['bb_position'] < 0.08):
        return "skip"
    
    return prediction