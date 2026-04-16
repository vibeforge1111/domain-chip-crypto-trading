def guard(features: dict, prediction: str) -> str:
    # Skip if candle has low conviction (small body relative to range)
    if features.get('body_ratio', 1) < 0.25:
        return "skip"
    
    # Skip if at extreme BB position but weak trend (choppy market)
    if (features.get('bb_position', 0.5) < 0.15 or features.get('bb_position', 0.5) > 0.85) and features.get('trend_strength', 1) < 0.3:
        return "skip"
    
    return prediction