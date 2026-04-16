def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # BB position: >0.55 for long, <0.45 for short
    if prediction == "long" and features.get("bb_pct_b", 0.5) > 0.55:
        confirmations += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) < 0.45:
        confirmations += 1
    
    # VWAP: above for long, below for short
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    
    # Stochastic: oversold for long, overbought for short
    stoch_k = features.get("stoch_k", 50)
    if prediction == "long" and stoch_k < 30:
        confirmations += 1
    elif prediction == "short" and stoch_k > 70:
        confirmations += 1
    
    # OBV slope: positive for long, negative for short
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram: positive for long, negative for short
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # Require 2+ confirmations
    return prediction if confirmations >= 2 else "skip"