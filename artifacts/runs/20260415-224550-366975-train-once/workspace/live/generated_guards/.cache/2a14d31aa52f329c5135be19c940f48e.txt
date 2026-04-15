def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # BB position: above midpoint for long, below for short
    if features.get("bb_pct_b", 0.5) > 0.5 and prediction == "long":
        confirmations += 1
    elif features.get("bb_pct_b", 0.5) < 0.5 and prediction == "short":
        confirmations += 1
    
    # VWAP: above for long, below for short
    if features.get("vwap_deviation", 0) > 0 and prediction == "long":
        confirmations += 1
    elif features.get("vwap_deviation", 0) < 0 and prediction == "short":
        confirmations += 1
    
    # Stochastic: exiting oversold for long, exiting overbought for short
    if features.get("stoch_k", 50) > 20 and features.get("stoch_d", 50) > 20 and prediction == "long":
        confirmations += 1
    elif features.get("stoch_k", 50) < 80 and features.get("stoch_d", 50) < 80 and prediction == "short":
        confirmations += 1
    
    # OBV slope: positive for long, negative for short
    if features.get("obv_slope", 0) > 0 and prediction == "long":
        confirmations += 1
    elif features.get("obv_slope", 0) < 0 and prediction == "short":
        confirmations += 1
    
    # MACD histogram: positive for long, negative for short
    if features.get("macd_histogram", 0) > 0 and prediction == "long":
        confirmations += 1
    elif features.get("macd_histogram", 0) < 0 and prediction == "short":
        confirmations += 1
    
    # Require at least 2 confirmations
    if confirmations >= 2:
        return prediction
    return "skip"