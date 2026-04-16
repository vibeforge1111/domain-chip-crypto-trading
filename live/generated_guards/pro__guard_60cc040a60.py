def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation (2h context)
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and rsi_2h < 65:
        confirmations += 1
    elif prediction == "short" and rsi_2h > 35:
        confirmations += 1
    
    # Stochastic confirmation
    stoch_k = features.get("stoch_k", 50)
    if prediction == "long" and stoch_k < 80:
        confirmations += 1
    elif prediction == "short" and stoch_k > 20:
        confirmations += 1
    
    # VWAP deviation confirmation
    vwap_dev = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap_dev >= -0.005:
        confirmations += 1
    elif prediction == "short" and vwap_dev <= 0.005:
        confirmations += 1
    
    # OBV slope confirmation
    obv_slope = features.get("obv_slope", 0)
    if prediction == "long" and obv_slope >= 0:
        confirmations += 1
    elif prediction == "short" and obv_slope <= 0:
        confirmations += 1
    
    # MACD histogram confirmation
    macd_hist = features.get("macd_histogram", 0)
    if prediction == "long" and macd_hist >= 0:
        confirmations += 1
    elif prediction == "short" and macd_hist <= 0:
        confirmations += 1
    
    # Bollinger Band position confirmation
    bb_pct_b = features.get("bb_pct_b", 0.5)
    if prediction == "long" and bb_pct_b < 0.85:
        confirmations += 1
    elif prediction == "short" and bb_pct_b > 0.15:
        confirmations += 1
    
    if confirmations < 2:
        return "skip"
    return prediction