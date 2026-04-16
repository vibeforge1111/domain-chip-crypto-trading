def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    bullish_count += features.get("macd_histogram", 0) > 0
    bullish_count += features.get("obv_slope", 0) > 0
    bullish_count += features.get("vwap_deviation", 0) > 0.002
    bullish_count += features.get("rsi_2h", 50) > 50
    bullish_count += features.get("stoch_k", 50) < 80
    
    # Count bearish signals
    bearish_count = 0
    bearish_count += features.get("macd_histogram", 0) < 0
    bearish_count += features.get("obv_slope", 0) < 0
    bearish_count += features.get("vwap_deviation", 0) < -0.002
    bearish_count += features.get("rsi_2h", 50) < 50
    bearish_count += features.get("stoch_k", 50) > 20
    
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction