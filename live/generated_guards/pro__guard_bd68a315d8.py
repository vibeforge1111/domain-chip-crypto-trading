def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    longs = 0
    shorts = 0
    
    # RSI confirmation
    if features.get('rsi_14', 50) < 40:
        longs += 1
    elif features.get('rsi_14', 50) > 60:
        shorts += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 30:
        longs += 1
    elif features.get('stoch_k', 50) > 70:
        shorts += 1
    
    # VWAP confirmation
    if features.get('vwap_deviation', 0) > 0:
        longs += 1
    elif features.get('vwap_deviation', 0) < 0:
        shorts += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        longs += 1
    elif features.get('macd_histogram', 0) < 0:
        shorts += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        longs += 1
    elif features.get('obv_slope', 0) < 0:
        shorts += 1
    
    # 2h RSI confirmation
    if features.get('rsi_2h', 50) < 40:
        longs += 1
    elif features.get('rsi_2h', 50) > 60:
        shorts += 1
    
    # BB position confirmation
    bb_pos = features.get('bb_pct_b', 0.5)
    if bb_pos < 0.3:
        longs += 1
    elif bb_pos > 0.7:
        shorts += 1
    
    # Skip if 2+ opposing signals
    if prediction == "long" and shorts >= 2:
        return "skip"
    if prediction == "short" and longs >= 2:
        return "skip"
    
    return prediction