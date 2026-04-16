def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # RSI confirmation (2h context)
    rsi_2h = features.get("rsi_2h", 50)
    if prediction == "long" and 30 < rsi_2h < 70:
        confirmations += 1
    elif prediction == "short" and 30 < rsi_2h < 70:
        confirmations += 1
    
    # Stochastic alignment
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    if prediction == "long" and stoch_k > stoch_d:
        confirmations += 1
    elif prediction == "short" and stoch_k < stoch_d:
        confirmations += 1
    
    # VWAP deviation check
    vwap_dev = features.get("vwap_deviation", 0)
    if prediction == "long" and vwap_dev > -0.01:
        confirmations += 1
    elif prediction == "short" and vwap_dev < 0.01:
        confirmations += 1
    
    # OBV momentum confirmation
    obv_slope = features.get("obv_slope", 0)
    if prediction == "long" and obv_slope > 0:
        confirmations += 1
    elif prediction == "short" and obv_slope < 0:
        confirmations += 1
    
    # MACD histogram confirmation
    macd_hist = features.get("macd_histogram", 0)
    if prediction == "long" and macd_hist > 0:
        confirmations += 1
    elif prediction == "short" and macd_hist < 0:
        confirmations += 1
    
    # Require 2+ confirmations
    if confirmations < 2:
        return "skip"
    return prediction