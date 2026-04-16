def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating using macd_histogram."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip if momentum is reversing (negative macd histogram)
    if macd_hist < 0:
        return "skip"
    
    # Skip if momentum weakening (near-zero) and stoch divergence
    if abs(macd_hist) < 0.0003 and abs(stoch_k - stoch_d) > 15:
        return "skip"
    
    # Skip if far from VWAP (exhaustion risk) with weak momentum
    if abs(vwap_dev) > 0.01 and macd_hist < 0.001:
        return "skip"
    
    return prediction