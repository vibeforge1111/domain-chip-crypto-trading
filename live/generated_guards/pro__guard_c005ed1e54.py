def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) < 70:
        bullish += 1
    if features.get('rsi_14', 50) > 30:
        bearish += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 80:
        bullish += 1
    if features.get('stoch_k', 50) > 20:
        bearish += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) >= -0.001:
        bullish += 1
    if features.get('vwap_deviation', 0) <= 0.001:
        bearish += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        bullish += 1
    if features.get('obv_slope', 0) < 0:
        bearish += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    if features.get('macd_histogram', 0) < 0:
        bearish += 1
    
    # RSI 2h wider context confirmation
    if features.get('rsi_2h', 50) < 70:
        bullish += 1
    if features.get('rsi_2h', 50) > 30:
        bearish += 1
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction