def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic confirmation
    if prediction == "long" and features.get("stoch_k", 50) < 30:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 70:
        confirmations += 1
    
    # Bollinger Band position confirmation
    if prediction == "long" and features.get("bb_pct_b", 0.5) < 0.2:
        confirmations += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) > 0.8:
        confirmations += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # Require 2+ confirmations
    return prediction if confirmations >= 2 else "skip"