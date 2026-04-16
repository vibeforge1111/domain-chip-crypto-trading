def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation (not overbought/oversold)
    if features.get('rsi_14', 50) < 70:
        bullish_count += 1
    if features.get('rsi_14', 50) > 30:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 80:
        bullish_count += 1
    if features.get('stoch_k', 50) > 20:
        bearish_count += 1
    
    # VWAP confirmation
    if features.get('vwap_deviation', 0) > 0:
        bullish_count += 1
    if features.get('vwap_deviation', 0) < 0:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    if features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # Require at least 2 confirmations
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction