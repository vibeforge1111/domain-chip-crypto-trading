def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish signals
    bullish = 0
    bearish = 0
    
    # Bollinger Band position
    if features.get("bb_pct_b", 0.5) > 0.6:
        bullish += 1
    elif features.get("bb_pct_b", 0.5) < 0.4:
        bearish += 1
    
    # VWAP deviation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) > 60:
        bullish += 1
    elif features.get("stoch_k", 50) < 40:
        bearish += 1
    
    # MACD histogram direction
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # RSI 2h trend
    if features.get("rsi_2h", 50) > 55:
        bullish += 1
    elif features.get("rsi_2h", 50) < 45:
        bearish += 1
    
    # Require at least 2 signals aligned with prediction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction