def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    agreements = 0
    
    # VWAP alignment (price above/below VWAP)
    if features.get("vwap_deviation", 0) > 0.001 and prediction == "long":
        agreements += 1
    elif features.get("vwap_deviation", 0) < -0.001 and prediction == "short":
        agreements += 1
    
    # MACD histogram alignment
    if features.get("macd_histogram", 0) > 0 and prediction == "long":
        agreements += 1
    elif features.get("macd_histogram", 0) < 0 and prediction == "short":
        agreements += 1
    
    # OBV slope alignment (volume confirms direction)
    if features.get("obv_slope", 0) > 0 and prediction == "long":
        agreements += 1
    elif features.get("obv_slope", 0) < 0 and prediction == "short":
        agreements += 1
    
    # Stochastic not in extreme territory
    if 20 < features.get("stoch_k", 50) < 80:
        agreements += 1
    
    # RSI 2h confirmation (wider timeframe trend)
    if prediction == "long" and features.get("rsi_2h", 50) > 50:
        agreements += 1
    elif prediction == "short" and features.get("rsi_2h", 50) < 50:
        agreements += 1
    
    # Require 2+ indicators to agree
    if agreements >= 2:
        return prediction
    return "skip"