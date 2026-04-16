def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 30:
        bullish += 1
    elif features.get('stoch_k', 50) > 70:
        bearish += 1
    
    # Stochastic crossover
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bullish += 1
    else:
        bearish += 1
    
    # VWAP deviation
    if features.get('vwap_deviation', 0) < -0.002:
        bullish += 1
    elif features.get('vwap_deviation', 0) > 0.002:
        bearish += 1
    
    # OBV slope
    if features.get('obv_slope', 0) > 0:
        bullish += 1
    else:
        bearish += 1
    
    # MACD histogram
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    else:
        bearish += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction