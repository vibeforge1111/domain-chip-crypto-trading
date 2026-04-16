def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # Stoch momentum alignment
    if features.get("stoch_k", 50) > features.get("stoch_d", 50):
        bullish_count += 1
    elif features.get("stoch_k", 50) < features.get("stoch_d", 50):
        bearish_count += 1
    
    # OBV momentum
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # MACD histogram direction
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # VWAP position
    if features.get("vwap_deviation", 0) > 0:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < 0:
        bearish_count += 1
    
    # Require 2+ indicators to agree with direction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"