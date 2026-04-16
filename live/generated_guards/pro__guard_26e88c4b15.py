def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # BB position: not at extremes (30-70 range)
    if 0.2 < features.get("bb_pct_b", 0.5) < 0.8:
        confirmations += 1
    
    # VWAP: price not too far below
    if features.get("vwap_deviation", 0) > -0.005:
        confirmations += 1
    
    # Stochastic: %K and %D aligned, not extreme
    if abs(features.get("stoch_k", 50) - features.get("stoch_d", 50)) < 10:
        confirmations += 1
    
    # OBV: positive slope indicates accumulation
    if features.get("obv_slope", 0) > 0:
        confirmations += 1
    
    # MACD: histogram positive
    if features.get("macd_histogram", 0) > 0:
        confirmations += 1
    
    # RSI 2h: wider context not extreme
    if 35 < features.get("rsi_2h", 50) < 65:
        confirmations += 1
    
    # Require 2+ confirmations
    if confirmations < 2:
        return "skip"
    
    return prediction