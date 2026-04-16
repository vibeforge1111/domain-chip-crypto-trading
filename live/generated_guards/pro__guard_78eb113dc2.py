def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 30:
        bullish_count += 1
    if features.get("stoch_k", 50) > 70:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    if features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    if features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0:
        bullish_count += 1
    if features.get("vwap_deviation", 0) < 0:
        bearish_count += 1
    
    # RSI 2h confirmation
    if features.get("rsi_2h", 50) < 40:
        bullish_count += 1
    if features.get("rsi_2h", 50) > 60:
        bearish_count += 1
    
    # Bollinger position confirmation
    if features.get("bb_pct_b", 0.5) < 0.3:
        bullish_count += 1
    if features.get("bb_pct_b", 0.5) > 0.7:
        bearish_count += 1
    
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction