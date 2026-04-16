def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    agree = 0
    
    # VWAP direction
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        agree += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        agree += 1
    
    # Stochastic healthy zone
    sk = features.get("stoch_k", 50)
    sd = features.get("stoch_d", 50)
    if prediction == "long" and 20 < sk < 80 and 20 < sd < 80:
        agree += 1
    elif prediction == "short" and 20 < sk < 80 and 20 < sd < 80:
        agree += 1
    
    # OBV momentum
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        agree += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        agree += 1
    
    # MACD histogram
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        agree += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        agree += 1
    
    # Require 2+ signals
    if agree < 2:
        return "skip"
    return prediction