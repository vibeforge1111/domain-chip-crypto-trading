def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    long_agree = 0
    short_agree = 0
    
    # Stochastic: K above D = bullish
    if features.get("stoch_k", 50) > features.get("stoch_d", 50):
        long_agree += 1
    else:
        short_agree += 1
    
    # MACD histogram: positive = bullish
    if features.get("macd_histogram", 0) > 0:
        long_agree += 1
    else:
        short_agree += 1
    
    # OBV slope: positive = bullish
    if features.get("obv_slope", 0) > 0:
        long_agree += 1
    else:
        short_agree += 1
    
    # VWAP: below VWAP (negative deviation) = bullish
    if features.get("vwap_deviation", 0) < 0:
        long_agree += 1
    else:
        short_agree += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and long_agree >= 2:
        return prediction
    if prediction == "short" and short_agree >= 2:
        return prediction
    
    return "skip"