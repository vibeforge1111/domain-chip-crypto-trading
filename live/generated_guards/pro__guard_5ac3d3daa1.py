def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum decelerates despite signal."""
    macd_histogram = features.get("macd_histogram", 0)
    rsi_14 = features.get("rsi_14", 50)
    obv_slope = features.get("obv_slope", 0)
    
    if prediction == "long":
        # Reject longs when macd histogram is negative (bearish momentum)
        if macd_histogram < -0.0001:
            return "skip"
        # Reject longs when momentum diverges: rising MACD but falling OBV
        if macd_histogram > 0 and obv_slope < 0:
            return "skip"
            
    elif prediction == "short":
        # Reject shorts when macd histogram is positive (bullish momentum)
        if macd_histogram > 0.0001:
            return "skip"
        # Reject shorts when momentum diverges: falling MACD but rising OBV
        if macd_histogram < 0 and obv_slope > 0:
            return "skip"
    
    return prediction