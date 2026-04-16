def guard(features: dict, prediction: str) -> str:
    """Guard: skip trades against OBV volume flow direction."""
    obv_slope = features.get("obv_slope", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip long trades when OBV slope is negative (selling pressure)
    if prediction == "long" and obv_slope < -0.5:
        return "skip"
    
    # Skip short trades when OBV slope is positive (buying pressure)
    if prediction == "short" and obv_slope > 0.5:
        return "skip"
    
    # Additional filter: skip longs if RSI in wider timeframe is overbought
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    return prediction