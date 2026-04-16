def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip trades when OBV is flat (no clear volume flow)
    if abs(obv_slope) < 0.001:
        return "skip"
    
    # Skip longs when OBV is declining (distribution)
    if prediction == "long" and obv_slope < 0:
        return "skip"
    
    # Skip shorts when OBV is rising (accumulation)
    if prediction == "short" and obv_slope > 0:
        return "skip"
    
    # Additional filter: skip longs when broader RSI is bearish
    if prediction == "long" and rsi_2h < 40:
        return "skip"
    
    # Additional filter: skip shorts when broader RSI is bullish
    if prediction == "short" and rsi_2h > 60:
        return "skip"
    
    return prediction