def guard(features: dict, prediction: str) -> str:
    """Filter trades where price is at Bollinger Band extreme but trend is weak."""
    bb_extreme = features['bb_position'] > 0.9 or features['bb_position'] < 0.1
    weak_trend = features['trend_strength'] < 0.3
    
    if bb_extreme and weak_trend:
        return "skip"
    return prediction