def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # RSI confirmation
    rsi = features.get('rsi_14', 50)
    if rsi < 70:
        bullish += 1
    if rsi > 30:
        bearish += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 80:
        bullish += 1
    if features.get('stoch_k', 50) > 20:
        bearish += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) > 0:
        bullish += 1
    if features.get('vwap_deviation', 0) < 0:
        bearish += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish += 1
    if features.get('macd_histogram', 0) < 0:
        bearish += 1
    
    # 2-hour RSI context confirmation
    if features.get('rsi_2h', 50) < 70:
        bullish += 1
    if features.get('rsi_2h', 50) > 30:
        bearish += 1
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction