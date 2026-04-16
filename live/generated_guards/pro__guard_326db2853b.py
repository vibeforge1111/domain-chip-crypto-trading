def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip longs if volume flow is bearish and wider timeframe also bearish
    if prediction == "long" and obv_slope < -0.05 and rsi_2h < 50:
        return "skip"
    
    # Skip shorts if volume flow is bullish and wider timeframe also bullish
    if prediction == "short" and obv_slope > 0.05 and rsi_2h > 50:
        return "skip"
    
    return prediction