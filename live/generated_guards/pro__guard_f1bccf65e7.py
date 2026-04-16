def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # BB position: longs need not be at extreme lows, shorts need not be at extreme highs
    if prediction == "long" and features.get("bb_pct_b", 0.5) > 0.15:
        confirmations += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) < 0.85:
        confirmations += 1
    
    # VWAP: longs above/near VWAP, shorts below/near VWAP
    if prediction == "long" and features.get("vwap_deviation", 0) > -0.003:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0.003:
        confirmations += 1
    
    # Stochastic momentum: reject if extremely oversold/overbought extremes
    if prediction == "long" and 15 < features.get("stoch_k", 50) < 85:
        confirmations += 1
    elif prediction == "short" and 15 < features.get("stoch_k", 50) < 85:
        confirmations += 1
    
    # OBV slope: positive for longs, negative for shorts
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram: positive for longs, negative for shorts
    if prediction == "long" and features.get("macd_histogram", 0) > -0.0001:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0.0001:
        confirmations += 1
    
    # Require 2+ confirming signals
    if confirmations >= 2:
        return prediction
    return "skip"