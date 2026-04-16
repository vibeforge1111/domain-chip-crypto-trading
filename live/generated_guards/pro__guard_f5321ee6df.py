def guard(features: dict, prediction: str) -> str:
    """Filter trades where wick dominance contradicts trend direction."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    ema_slope = features.get('ema_slope', 0)
    trend_strength = features.get('trend_strength', 0)
    
    # Skip if trend is weak but candle structure is extreme
    if trend_strength < 0.3 and abs(upper_wick - lower_wick) > 0.2:
        return "skip"
    
    # Wick dominance vs trend alignment
    wick_dominance = upper_wick - lower_wick
    
    # In uptrend, lower wicks should dominate for long signals
    if prediction == "long" and ema_slope > 0 and wick_dominance > 0.1:
        return "skip"
    
    # In downtrend, upper wicks should dominate for short signals
    if prediction == "short" and ema_slope < 0 and wick_dominance < -0.1:
        return "skip"
    
    return prediction