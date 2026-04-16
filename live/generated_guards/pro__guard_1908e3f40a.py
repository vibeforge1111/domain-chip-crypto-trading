def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # RSI conditions
    if features.get('rsi_14', 50) < 70:
        bullish_count += 1
    if features.get('rsi_14', 50) > 30:
        bearish_count += 1
    
    # Stochastic conditions
    if features.get('stoch_k', 50) < 80:
        bullish_count += 1
    if features.get('stoch_k', 50) > 20:
        bearish_count += 1
    
    # VWAP deviation
    if features.get('vwap_deviation', 0) > 0:
        bullish_count += 1
    if features.get('vwap_deviation', 0) < 0:
        bearish_count += 1
    
    # MACD histogram
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    if features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # OBV slope
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    if features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # Require 2+ confirmations matching prediction direction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    if prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"