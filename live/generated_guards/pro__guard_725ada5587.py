def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # VWAP alignment
    if features['vwap_deviation'] > 0:
        bullish_count += 1
    elif features['vwap_deviation'] < 0:
        bearish_count += 1
    
    # MACD histogram alignment
    if features['macd_histogram'] > 0:
        bullish_count += 1
    elif features['macd_histogram'] < 0:
        bearish_count += 1
    
    # Stochastic alignment
    if features['stoch_k'] < 70:
        bullish_count += 1
    elif features['stoch_k'] > 30:
        bearish_count += 1
    
    # RSI confirmation
    if features['rsi_14'] < 65:
        bullish_count += 1
    elif features['rsi_14'] > 35:
        bearish_count += 1
    
    # OBV momentum
    if features['obv_slope'] > 0:
        bullish_count += 1
    elif features['obv_slope'] < 0:
        bearish_count += 1
    
    # Require 2+ confirmations
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"