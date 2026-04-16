def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Skip shorts when OBV shows accumulation (positive slope + positive MACD)
    if prediction == "short" and obv_slope > 0.05 and macd_histogram > 0:
        return "skip"
    
    # Skip longs when OBV shows distribution (negative slope + negative MACD)
    if prediction == "long" and obv_slope < -0.05 and macd_histogram < 0:
        return "skip"
    
    return prediction