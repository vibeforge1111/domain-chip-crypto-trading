def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish confirmations
    bullish = 0
    bearish = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 30:
        bullish += 1
    elif features.get("rsi_14", 50) > 70:
        bearish += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 20 and features.get("stoch_d", 50) < 20:
        bullish += 1
    elif features.get("stoch_k", 80) > 80 and features.get("stoch_d", 80) > 80:
        bearish += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # Bollinger Band position confirmation
    if features.get("bb_pct_b", 0.5) < 0.2:
        bullish += 1
    elif features.get("bb_pct_b", 0.5) > 0.8:
        bearish += 1
    
    # Require 2+ signals to agree with direction
    if prediction == "long" and bullish >= 2:
        return prediction
    elif prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"