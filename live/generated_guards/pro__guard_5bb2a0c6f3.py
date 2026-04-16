def guard(features: dict, prediction: str) -> str:
    """Filter signals with momentum/trend divergence and weak volume confirmation."""
    stoch_k = features.get('stoch_k', 50)
    rsi_14 = features.get('rsi_14', 50)
    ema_slope = features.get('ema_slope', 0)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    # Skip long if RSI overbought and trend slope disagrees
    if prediction == 'long' and rsi_14 > 70 and ema_slope < 0:
        return "skip"
    # Skip short if RSI oversold and trend slope disagrees
    if prediction == 'short' and rsi_14 < 30 and ema_slope > 0:
        return "skip"
    # Skip if extreme stochastic without volume confirmation
    if (stoch_k > 85 or stoch_k < 15) and volume_ratio < 0.7:
        return "skip"
    
    return prediction