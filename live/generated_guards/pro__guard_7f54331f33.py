def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish confirmations
    bullish_count = 0
    bullish_count += features.get("vwap_deviation", 0) < 0  # Price below VWAP
    bullish_count += features.get("stoch_k", 50) < 30  # Oversold
    bullish_count += features.get("obv_slope", 0) > 0  # Positive OBV
    bullish_count += features.get("macd_histogram", 0) > 0  # Bullish MACD
    
    # Count bearish confirmations
    bearish_count = 0
    bearish_count += features.get("vwap_deviation", 0) > 0  # Price above VWAP
    bearish_count += features.get("stoch_k", 50) > 70  # Overbought
    bearish_count += features.get("bb_pct_b", 0.5) > 0.8  # Near upper BB
    bearish_count += features.get("macd_histogram", 0) < 0  # Bearish MACD
    
    if prediction == "long" and bullish_count >= 2:
        return prediction
    if prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"