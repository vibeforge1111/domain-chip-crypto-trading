def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic confirmation (not extreme)
    if prediction == "long" and features.get("stoch_k", 50) > 20 and features.get("stoch_k", 50) < 80:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 20 and features.get("stoch_k", 50) < 80:
        confirmations += 1
    
    # VWAP deviation alignment
    if prediction == "long" and features.get("vwap_deviation", 0) > -0.005:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0.005:
        confirmations += 1
    
    # OBV momentum confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        confirmations += 1
    
    # MACD histogram alignment
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmations += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmations += 1
    
    # RSI 2h broader context confirmation
    if prediction == "long" and 30 < features.get("rsi_2h", 50) < 70:
        confirmations += 1
    elif prediction == "short" and 30 < features.get("rsi_2h", 50) < 70:
        confirmations += 1
    
    # BB position boundary check
    bb_pos = features.get("bb_pct_b", 0.5)
    if prediction == "long" and bb_pos < 0.85:
        confirmations += 1
    elif prediction == "short" and bb_pos > 0.15:
        confirmations += 1
    
    return "skip" if confirmations < 2 else prediction