def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) > 50:
        bullish_signals += 1
    elif features.get('rsi_14', 50) < 50:
        bearish_signals += 1
    
    # MACD momentum alignment
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_signals += 1
    
    # VWAP position
    if features.get('vwap_deviation', 0) > 0:
        bullish_signals += 1
    elif features.get('vwap_deviation', 0) < 0:
        bearish_signals += 1
    
    # Bollinger Band position
    if features.get('bb_pct_b', 0.5) > 0.5:
        bullish_signals += 1
    elif features.get('bb_pct_b', 0.5) < 0.5:
        bearish_signals += 1
    
    # OBV trend direction
    if features.get('obv_slope', 0) > 0:
        bullish_signals += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bullish_signals += 1
    elif features.get('stoch_k', 50) < features.get('stoch_d', 50):
        bearish_signals += 1
    
    # Require at least 2 signals aligned with prediction
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    elif prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction