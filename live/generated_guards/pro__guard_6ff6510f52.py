def guard(features: dict, prediction: str) -> str:
    """Skip trades too close to VWAP fair value or misaligned with wider RSI context."""
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if too close to fair value (low VWAP deviation)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # For longs, require bullish wider RSI context; for shorts, bearish
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    return prediction