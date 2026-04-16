def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # VWAP confirmation
    if features.get('vwap_deviation', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Require at least 2 signals to agree with prediction
    if prediction == "long" and bearish_signals >= 2:
        return "skip"
    if prediction == "short" and bullish_signals >= 2:
        return "skip"
    
    return prediction