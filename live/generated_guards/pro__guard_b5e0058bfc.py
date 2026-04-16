def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    pos_count = 0
    neg_count = 0
    
    # VWAP alignment
    if features['vwap_deviation'] > 0:
        pos_count += 1
    elif features['vwap_deviation'] < 0:
        neg_count += 1
    
    # Stochastic confirmation
    if features['stoch_k'] > 30 and features['stoch_d'] > 30:
        pos_count += 1
    elif features['stoch_k'] < 70 and features['stoch_d'] < 70:
        neg_count += 1
    
    # OBV momentum
    if features['obv_slope'] > 0:
        pos_count += 1
    elif features['obv_slope'] < 0:
        neg_count += 1
    
    # MACD direction
    if features['macd_histogram'] > 0:
        pos_count += 1
    elif features['macd_histogram'] < 0:
        neg_count += 1
    
    # BB position
    if features['bb_pct_b'] > 0.3:
        pos_count += 1
    elif features['bb_pct_b'] < 0.7:
        neg_count += 1
    
    # 2h RSI context
    if features['rsi_2h'] < 70:
        pos_count += 1
    elif features['rsi_2h'] > 30:
        neg_count += 1
    
    if prediction == "long" and pos_count >= 2:
        return prediction
    if prediction == "short" and neg_count >= 2:
        return prediction
    return "skip"