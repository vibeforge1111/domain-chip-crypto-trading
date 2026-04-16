def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0:
        bullish += 1
    elif features.get("vwap_deviation", 0) < 0:
        bearish += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 20:
        bullish += 1
    elif features.get("stoch_k", 50) > 80:
        bearish += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    elif features.get("obv_slope", 0) < 0:
        bearish += 1
    
    # Require 2+ aligned signals
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction