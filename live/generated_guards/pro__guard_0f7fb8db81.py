def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs when OBV is declining (distribution)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    # Extra filter: avoid longs when 2H RSI is overbought
    if prediction == "long" and rsi_2h > 80:
        return "skip"
    
    # Extra filter: avoid shorts when 2H RSI is oversold
    if prediction == "short" and rsi_2h < 20:
        return "skip"
    
    return prediction