def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish confirmations
    bullish = 0
    bearish = 0
    
    # RSI confirmation
    rsi = features.get("rsi_2h", 50)
    if rsi < 65:
        bullish += 1
    elif rsi > 35:
        bearish += 1
    
    # VWAP deviation confirmation
    vwap_dev = features.get("vwap_deviation", 0)
    if vwap_dev > 0.001:
        bullish += 1
    elif vwap_dev < -0.001:
        bearish += 1
    
    # Stochastic confirmation
    stoch = features.get("stoch_k", 50)
    if stoch < 75:
        bullish += 1
    elif stoch > 25:
        bearish += 1
    
    # MACD histogram confirmation
    macd = features.get("macd_histogram", 0)
    if macd > 0:
        bullish += 1
    elif macd < 0:
        bearish += 1
    
    # OBV slope confirmation
    obv = features.get("obv_slope", 0)
    if obv > 0:
        bullish += 1
    elif obv < 0:
        bearish += 1
    
    # Require 2+ indicators to agree with prediction direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction