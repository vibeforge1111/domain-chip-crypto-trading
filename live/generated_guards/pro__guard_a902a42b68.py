def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum-trend divergence, weak volume, or extreme volatility."""
    # Skip if momentum contradicts trend direction
    momentum_dir = 1 if features['momentum_score'] > 0.3 else (-1 if features['momentum_score'] < -0.3 else 0)
    trend_dir = 1 if features['ema_slope'] > 0 else (-1 if features['ema_slope'] < 0 else 0)
    if momentum_dir != 0 and momentum_dir != trend_dir:
        return "skip"
    
    # Skip if candle is wick-dominant (low body ratio, high wicks)
    if features['body_ratio'] < 0.35 and (features['upper_wick_ratio'] + features['lower_wick_ratio']) > 0.45:
        return "skip"
    
    # Skip if volume is weak
    if features['volume_ratio'] < 0.8:
        return "skip"
    
    # Skip if extreme momentum with extreme volatility (whipsaw risk)
    if abs(features['momentum_score']) > 0.75 and features['volatility_regime'] > 0.75:
        return "skip"
    
    return prediction