def guard(features: dict, prediction: str) -> str:
    """Filter trades based on wick rejection and momentum confirmation."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 0)
    
    if prediction == "skip":
        return prediction
    
    # Reject if wicks dominate the candle (weak/absorbing candle)
    total_wick = upper_wick + lower_wick
    if total_wick > 0.7 and body_ratio < 0.3:
        return "skip"
    
    # Reject signals when momentum contradicts direction
    ema_slope = features.get('ema_slope', 0)
    rsi_14 = features.get('rsi_14', 50)
    
    if prediction == "long":
        if ema_slope < 0 and rsi_14 < 45:
            return "skip"
    elif prediction == "short":
        if ema_slope > 0 and rsi_14 > 55:
            return "skip"
    
    return prediction