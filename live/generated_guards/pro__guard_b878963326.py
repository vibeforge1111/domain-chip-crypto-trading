def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish signals
    bullish = 0
    bearish = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 65:
        bullish += 1
    elif features.get("rsi_14", 50) > 35:
        bearish += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 75:
        bullish += 1
    elif features.get("stoch_k", 50) > 25:
        bearish += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.002:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        bearish += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # 2h RSI confirmation
    if features.get("rsi_2h", 50) < 70:
        bullish += 1
    elif features.get("rsi_2h", 50) > 30:
        bearish += 1
    
    # Require at least 2 signals to agree with direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction