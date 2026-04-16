def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_confirmations = 0
    bearish_confirmations = 0
    
    # Stochastic confirmation (bullish if %K > %D)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    if stoch_k > stoch_d:
        bullish_confirmations += 1
    elif stoch_k < stoch_d:
        bearish_confirmations += 1
    
    # VWAP deviation confirmation
    vwap_dev = features.get('vwap_deviation', 0)
    if vwap_dev > 0.001:
        bullish_confirmations += 1
    elif vwap_dev < -0.001:
        bearish_confirmations += 1
    
    # MACD histogram confirmation
    macd = features.get('macd_histogram', 0)
    if macd > 0:
        bullish_confirmations += 1
    elif macd < 0:
        bearish_confirmations += 1
    
    # OBV slope confirmation
    obv = features.get('obv_slope', 0)
    if obv > 0:
        bullish_confirmations += 1
    elif obv < 0:
        bearish_confirmations += 1
    
    # Require 2+ confirmations matching the direction
    if prediction == "long" and bullish_confirmations >= 2:
        return prediction
    elif prediction == "short" and bearish_confirmations >= 2:
        return prediction
    
    return "skip"