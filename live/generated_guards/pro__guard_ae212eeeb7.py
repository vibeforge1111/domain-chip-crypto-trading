def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # Stochastic momentum
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # MACD histogram direction
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # VWAP deviation
    if features.get('vwap_deviation', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # OBV momentum
    if features.get('obv_slope', 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Require 2+ indicators to agree with direction
    if prediction == "long" and bullish_signals >= 2:
        return prediction
    elif prediction == "short" and bearish_signals >= 2:
        return prediction
    
    return "skip"