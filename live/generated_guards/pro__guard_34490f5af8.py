def guard(features: dict, prediction: str) -> str:
    """Skip trades when volume flow (OBV) opposes trade direction."""
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Long trades: skip if OBV slope negative and RSI not oversold
    if prediction == "long" and obv_slope < -0.1 and rsi_2h > 40:
        return "skip"
    
    # Short trades: skip if OBV slope positive and RSI not overbought
    if prediction == "short" and obv_slope > 0.1 and rsi_2h < 60:
        return "skip"
    
    return prediction