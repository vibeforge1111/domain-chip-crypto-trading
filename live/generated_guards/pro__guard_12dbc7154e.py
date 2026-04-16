def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish signals
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 25:
        bullish_count += 1
    if features.get("stoch_k", 50) > 75:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish_count += 1
    
    # Bollinger position confirmation
    if features.get("bb_pct_b", 0.5) < 0.25:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.75:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # Wider RSI confirmation
    if features.get("rsi_2h", 50) < 40:
        bullish_count += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish_count += 1
    
    # Require at least 2 confirmations
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"