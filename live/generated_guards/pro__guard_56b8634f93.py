def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    # Count bearish signals
    bearish_count = 0
    
    # Stochastic oscillators
    if features.get("stoch_k", 50) < 70:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 30:
        bearish_count += 1
    
    # MACD histogram
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # OBV slope (volume accumulation/distribution)
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # VWAP deviation
    if features.get("vwap_deviation", 0) > 0:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < 0:
        bearish_count += 1
    
    # Bollinger Band position
    if features.get("bb_pct_b", 0.5) < 0.7:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.3:
        bearish_count += 1
    
    # Require at least 2 signals to agree with prediction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction