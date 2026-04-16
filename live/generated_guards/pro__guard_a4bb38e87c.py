def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    agree = 0
    
    # RSI in favorable range
    if prediction == "long" and features.get("rsi_14", 50) < 70:
        agree += 1
    elif prediction == "short" and features.get("rsi_14", 50) > 30:
        agree += 1
    
    # Stochastic not extreme
    if prediction == "long" and features.get("stoch_k", 50) < 80:
        agree += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 20:
        agree += 1
    
    # VWAP alignment
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        agree += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        agree += 1
    
    # BB position alignment
    if prediction == "long" and features.get("bb_pct_b", 0.5) < 0.7:
        agree += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) > 0.3:
        agree += 1
    
    # MACD direction
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        agree += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        agree += 1
    
    # 2H RSI confirmation
    if prediction == "long" and features.get("rsi_2h", 50) < 65:
        agree += 1
    elif prediction == "short" and features.get("rsi_2h", 50) > 35:
        agree += 1
    
    return prediction if agree >= 2 else "skip"