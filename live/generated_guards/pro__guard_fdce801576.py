def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    macd_hist = features.get('macd_histogram', 0)
    
    # Skip longs when OBV shows distribution (negative slope)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"
    
    # Skip shorts when OBV shows accumulation (positive slope)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"
    
    # Additional filter: skip longs with bearish MACD histogram
    if prediction == "long" and macd_hist < -0.0005:
        return "skip"
    
    # Additional filter: skip shorts with bullish MACD histogram
    if prediction == "short" and macd_hist > 0.0005:
        return "skip"
    
    return prediction