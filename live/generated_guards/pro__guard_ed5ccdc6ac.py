def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    macd_histogram = features.get("macd_histogram", 0)
    obv_slope = features.get("obv_slope", 0)
    
    # Only trade at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Long entries: require price below VWAP, positive momentum, and positive volume trend
    if prediction == "long" and bb_pct_b < 0.05:
        if vwap_deviation >= 0 or macd_histogram <= 0 or obv_slope <= 0:
            return "skip"
    
    # Short entries: require price above VWAP, negative momentum, and negative volume trend
    if prediction == "short" and bb_pct_b > 0.95:
        if vwap_deviation <= 0 or macd_histogram >= 0 or obv_slope >= 0:
            return "skip"
    
    return prediction