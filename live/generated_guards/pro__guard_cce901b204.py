def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    
    bullish_count = 0
    bearish_count = 0
    
    # Bollinger Bands position
    if features.get('bb_pct_b', 0.5) < 0.2:
        bullish_count += 1
    elif features.get('bb_pct_b', 0.5) > 0.8:
        bearish_count += 1
    
    # Stochastic overbought/oversold
    if features.get('stoch_k', 50) < 20 and features.get('stoch_d', 50) < 20:
        bullish_count += 1
    elif features.get('stoch_k', 50) > 80 and features.get('stoch_d', 50) > 80:
        bearish_count += 1
    
    # OBV slope
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    elif features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # MACD histogram
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    elif features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # VWAP deviation
    if features.get('vwap_deviation', 0) < -0.005:
        bullish_count += 1
    elif features.get('vwap_deviation', 0) > 0.005:
        bearish_count += 1
    
    # RSI 2h context
    if features.get('rsi_2h', 50) < 35:
        bullish_count += 1
    elif features.get('rsi_2h', 50) > 65:
        bearish_count += 1
    
    if prediction == "long" and bullish_count < 2:
        return "skip"
    elif prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction