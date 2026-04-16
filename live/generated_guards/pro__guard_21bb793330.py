def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when OBV is declining (distribution) and 2h RSI not oversold
    if prediction == 'long' and obv_slope < -0.1 and rsi_2h > 40:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation) and 2h RSI not overbought
    if prediction == 'short' and obv_slope > 0.1 and rsi_2h < 60:
        return "skip"
    
    return prediction