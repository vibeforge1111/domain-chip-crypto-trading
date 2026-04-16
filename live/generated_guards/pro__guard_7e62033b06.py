def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # RSI 2h trend confirmation
    if features.get("rsi_2h", 50) > 52:
        bullish += 1
    elif features.get("rsi_2h", 50) < 48:
        bearish += 1
    
    # VWAP deviation confirms direction
    if features.get("vwap_deviation", 0) > 0.002:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        bearish += 1
    
    # Stochastic momentum - not overbought for longs, not oversold for shorts
    if features.get("stoch_k", 50) < 75:
        bullish += 1
    if features.get("stoch_k", 50) > 25:
        bearish += 1
    
    # MACD histogram confirms momentum
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # OBV slope confirms volume
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    elif features.get("obv_slope", 0) < 0:
        bearish += 1
    
    if prediction == "long" and bullish >= 2:
        return prediction
    elif prediction == "short" and bearish >= 2:
        return prediction
    return "skip"