def guard(features: dict, prediction: str) -> str:
    """Filter trades against momentum direction as indicated by macd_histogram."""
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip long when macd histogram negative (momentum bearish)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Skip short when macd histogram positive (momentum bullish)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    # Skip when stochastic divergence suggests exhaustion
    if stoch_k < 20 and stoch_d < 20 and prediction == "long":
        return "skip"
    if stoch_k > 80 and stoch_d > 80 and prediction == "short":
        return "skip"
    
    return prediction