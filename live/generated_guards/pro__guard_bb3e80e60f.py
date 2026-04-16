def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    agree_count = 0
    
    # RSI alignment (14 and 2h)
    if features['rsi_14'] > 55 and features['rsi_2h'] > 52:
        agree_count += 1
    elif features['rsi_14'] < 45 and features['rsi_2h'] < 48:
        agree_count += 1
    
    # Stochastic alignment
    if features['stoch_k'] > 60 and features['stoch_d'] > 55:
        agree_count += 1
    elif features['stoch_k'] < 40 and features['stoch_d'] < 45:
        agree_count += 1
    
    # Bollinger position
    if features['bb_pct_b'] > 0.75:
        agree_count += 1
    elif features['bb_pct_b'] < 0.25:
        agree_count += 1
    
    # VWAP deviation (price above VWAP for longs)
    if features['vwap_deviation'] > 0.003:
        agree_count += 1
    elif features['vwap_deviation'] < -0.003:
        agree_count += 1
    
    # MACD histogram direction
    if features['macd_histogram'] > 0.0005:
        agree_count += 1
    elif features['macd_histogram'] < -0.0005:
        agree_count += 1
    
    return prediction if agree_count >= 2 else "skip"