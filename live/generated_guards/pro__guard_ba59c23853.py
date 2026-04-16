def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # Momentum confirmation
    if features.get('rsi_14', 50) < 65:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    if features.get('stoch_k', 50) < 70:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Trend confirmation via VWAP
    if features.get('vwap_deviation', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Momentum via MACD
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Wider context via 2h RSI
    if features.get('rsi_2h', 50) < 60:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals < 3:
        return "skip"
    if prediction == "short" and bearish_signals < 3:
        return "skip"
    
    return prediction