def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) >= 50:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # Stochastic momentum
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bullish_count += 1
    else:
        bearish_count += 1
    
    # OBV trend confirmation
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    else:
        bearish_count += 1
    
    # Validate against prediction direction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    if prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"