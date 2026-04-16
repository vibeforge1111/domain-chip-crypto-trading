def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV momentum direction."""
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # Skip long if OBV declining (distribution) and MACD bearish
    if prediction == "long" and obv_slope < -0.01 and macd_histogram < 0:
        return "skip"
    
    # Skip short if OBV rising (accumulation) and MACD bullish
    if prediction == "short" and obv_slope > 0.01 and macd_histogram > 0:
        return "skip"
    
    return prediction