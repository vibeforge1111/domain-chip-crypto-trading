def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme Bollinger positions with weak trend confirmation."""
    bb_extreme = features['bb_position'] < 0.1 or features['bb_position'] > 0.9
    weak_trend = features['trend_strength'] < 0.3 and abs(features['ema_slope']) < 0.001
    
    if bb_extreme and weak_trend:
        return "skip"
    
    return prediction