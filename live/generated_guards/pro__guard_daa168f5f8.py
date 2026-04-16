def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Bollinger Bands position
    if features.get("bb_pct_b", 0.5) > 0.6:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) < 0.4:
        bearish_count += 1
    
    # VWAP deviation
    if features.get("vwap_deviation", 0) > 0.002:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) > 60 and features.get("stoch_d", 50) > 50:
        bullish_count += 1
    elif features.get("stoch_k", 50) < 40 and features.get("stoch_d", 50) < 50:
        bearish_count += 1
    
    # OBV slope
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # MACD histogram
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # RSI 2h confirmation
    if features.get("rsi_2h", 50) > 55:
        bullish_count += 1
    elif features.get("rsi_2h", 50) < 45:
        bearish_count += 1
    
    # Require 2+ signals to agree with direction
    if prediction == "long" and bearish_count >= 2:
        return "skip"
    if prediction == "short" and bullish_count >= 2:
        return "skip"
    
    return prediction