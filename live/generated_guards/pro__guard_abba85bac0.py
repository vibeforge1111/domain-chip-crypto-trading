def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and momentum disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    macd = features.get("macd_histogram", 0)
    obv = features.get("obv_slope", 0)
    
    if prediction == "long":
        # Long is risky if price too far above VWAP AND momentum weak
        if vwap_dev > 0.008 and (stoch_k < 30 or macd < 0):
            return "skip"
    elif prediction == "short":
        # Short is risky if price too far below VWAP AND momentum strong
        if vwap_dev < -0.008 and (stoch_k > 70 or macd > 0):
            return "skip"
    
    return prediction