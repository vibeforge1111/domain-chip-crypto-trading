def guard(features: dict, prediction: str) -> str:
    """Filter trades lacking momentum alignment across indicators."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    stoch = features.get("stoch_k", 50)
    macd = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    
    if prediction == "short":
        if rsi > 40 and stoch > 40 and macd > 0:
            return "skip"
    elif prediction == "long":
        if rsi < 60 and stoch < 60 and macd < 0:
            return "skip"
    
    return prediction