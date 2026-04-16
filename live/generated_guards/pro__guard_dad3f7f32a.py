def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish confirmations
    bullish = 0
    bearish = 0
    
    # RSI 2H confirmation
    if features.get("rsi_2h", 50) > 52:
        bullish += 1
    elif features.get("rsi_2h", 50) < 48:
        bearish += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 25:
        bullish += 1
    elif features.get("stoch_k", 50) > 75:
        bearish += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.001:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.001:
        bearish += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    elif features.get("obv_slope", 0) < 0:
        bearish += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # BB position confirmation
    if features.get("bb_pct_b", 0.5) > 0.55:
        bullish += 1
    elif features.get("bb_pct_b", 0.5) < 0.45:
        bearish += 1
    
    # Require 2+ indicators to agree with prediction direction
    if prediction == "long" and bullish >= 2:
        return prediction
    elif prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"