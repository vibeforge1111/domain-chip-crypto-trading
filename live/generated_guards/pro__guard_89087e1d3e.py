def guard(features: dict, prediction: str) -> str:
    """Filter signals with bullish wick rejection in downtrend - potential fakeouts."""
    # Bullish rejection (large lower wick) in a downtrend (negative EMA) on high volume
    # often indicates a fakeout that traps buyers
    wick_imbalance = features.get('lower_wick_ratio', 0) - features.get('upper_wick_ratio', 0)
    volume_spike = features.get('volume_ratio', 1) > 1.2
    
    if wick_imbalance > 0.3 and volume_spike and features.get('ema_slope', 0) < 0:
        return "skip"
    return prediction