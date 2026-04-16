def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Momentum confirmations
    if features.get('rsi_14', 50) < 55:
        bullish += 1
    elif features.get('rsi_14', 50) > 45:
        bearish += 1
    
    if features.get('stoch_k', 50) < 70:
        bullish += 1
    elif features.get('stoch_k', 50) > 30:
        bearish += 1
    
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish += 1
    
    # Trend confirmations
    if features.get('vwap_deviation', 0) > 0:
        bullish += 1
    elif features.get('vwap_deviation', 0) < 0:
        bearish += 1
    
    if features.get('obv_slope', 0) > 0:
        bullish += 1
    elif features.get('obv_slope', 0) < 0:
        bearish += 1
    
    if features.get('rsi_2h', 50) < 55:
        bullish += 1
    elif features.get('rsi_2h', 50) > 45:
        bearish += 1
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction