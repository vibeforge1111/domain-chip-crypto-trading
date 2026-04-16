def guard(features: dict, prediction: str) -> str:
    """Filter out trades with suspicious candle structure (dominant wicks indicate indecision)."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 1)
    
    # Reject candles where wicks dominate (>60% combined) - high reversal risk
    if (upper_wick + lower_wick) > 0.6:
        return "skip"
    
    # Reject candles with very small bodies - no conviction
    if body_ratio < 0.25:
        return "skip"
    
    return prediction