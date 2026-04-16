def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # VWAP deviation
    if features.get('vwap_deviation', 0) > 0.002:
        bullish_count += 1
    elif features.get('vwap_deviation', 0) < -0.002:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) > 60 and features.get('stoch_d', 50) > 60:
        bullish_count += 1
    elif features.get('stoch_k', 50) < 40 and features.get('stoch_d', 50) < 40:
        bearish_count += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # RSI 2H wider context
    if features.get('rsi_2h', 50) > 55:
        bullish_count += 1
    elif features.get('rsi_2h', 50) < 45:
        bearish_count += 1
    
    # BB position (only confirm if not at extremes)
    bb_pos = features.get('bb_pct_b', 0.5)
    if 0.2 <= bb_pos <= 0.8:
        if bb_pos > 0.5:
            bullish_count += 1
        elif bb_pos < 0.5:
            bearish_count += 1
    
    # Require 2+ signals to agree with prediction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"