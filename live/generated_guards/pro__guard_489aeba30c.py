def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    bullish_count = 0
    bearish_count = 0
    
    # RSI 2H confirmation
    if features.get('rsi_2h', 50) < 35:
        bullish_count += 1
    elif features.get('rsi_2h', 50) > 65:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 25:
        bullish_count += 1
    elif features.get('stoch_k', 50) > 75:
        bearish_count += 1
    
    # Bollinger Band position confirmation
    if features.get('bb_pct_b', 0.5) < 0.2:
        bullish_count += 1
    elif features.get('bb_pct_b', 0.5) > 0.8:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) < -0.005:
        bullish_count += 1
    elif features.get('vwap_deviation', 0) > 0.005:
        bearish_count += 1
    
    # Require at least 2 aligned signals
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction