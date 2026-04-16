def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ aligned signals."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    if features.get('bb_pct_b', 0.5) < 0.3:
        bullish += 1
    elif features.get('bb_pct_b', 0.5) > 0.7:
        bearish += 1
    
    if features.get('vwap_deviation', 0) < -0.002:
        bullish += 1
    elif features.get('vwap_deviation', 0) > 0.002:
        bearish += 1
    
    if features.get('stoch_k', 50) < 25:
        bullish += 1
    elif features.get('stoch_k', 50) > 75:
        bearish += 1
    
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish += 1
    
    if features.get('rsi_2h', 50) < 35:
        bullish += 1
    elif features.get('rsi_2h', 50) > 65:
        bearish += 1
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction