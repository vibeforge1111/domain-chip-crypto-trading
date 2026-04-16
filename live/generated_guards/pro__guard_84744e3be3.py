def guard(features: dict, prediction: str) -> str:
    """Filter signals based on candle structure quality and momentum alignment."""
    # High wick dominance suggests rejection/uncertainty zones
    wick_dominance = features['upper_wick_ratio'] + features['lower_wick_ratio']
    if wick_dominance > 0.65:
        return "skip"
    
    # Weak momentum + weak trend = low conviction trade
    if features['momentum_score'] < 0.35 and features['trend_strength'] < 0.45:
        return "skip"
    
    # RSI extremes with weak trend alignment is dangerous
    if (features['rsi_14'] > 70 or features['rsi_14'] < 30) and abs(features['ema_slope']) < 0.001:
        return "skip"
    
    return prediction