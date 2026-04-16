def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation (not overbought/oversold)
    if features.get('rsi_14', 50) < 70:
        bullish_signals += 1
    if features.get('rsi_14', 50) > 30:
        bearish_signals += 1
    
    # Stochastic momentum direction
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # MACD histogram direction
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_signals += 1
    
    # OBV trend confirmation
    if features.get('obv_slope', 0) > 0:
        bullish_signals += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_signals += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) > 0:
        bullish_signals += 1
    elif features.get('vwap_deviation', 0) < 0:
        bearish_signals += 1
    
    # RSI_2h wider context
    if features.get('rsi_2h', 50) < 70:
        bullish_signals += 1
    if features.get('rsi_2h', 50) > 30:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction