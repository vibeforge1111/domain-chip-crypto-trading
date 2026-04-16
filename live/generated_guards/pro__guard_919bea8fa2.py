def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count confirming signals
    confirmations = 0
    
    # Stochastic overbought/oversold
    if features["stoch_k"] < 30 and features["stoch_d"] < 30:
        confirmations += 1
    elif features["stoch_k"] > 70 and features["stoch_d"] > 70:
        confirmations += 1
    
    # VWAP alignment
    if features["vwap_deviation"] > 0.002:
        confirmations += 1
    elif features["vwap_deviation"] < -0.002:
        confirmations += 1
    
    # OBV momentum
    if features["obv_slope"] > 0:
        confirmations += 1
    elif features["obv_slope"] < 0:
        confirmations += 1
    
    # MACD histogram direction
    if features["macd_histogram"] > 0:
        confirmations += 1
    elif features["macd_histogram"] < 0:
        confirmations += 1
    
    # RSI 2H context
    if features["rsi_2h"] < 40 or features["rsi_2h"] > 60:
        confirmations += 1
    
    # Require 2+ confirmations
    if confirmations >= 2:
        return prediction
    return "skip"