def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation
    if features["rsi_14"] < 70 and features["rsi_14"] > 40:
        bullish_signals += 1
    if features["rsi_14"] > 30 and features["rsi_14"] < 60:
        bearish_signals += 1
    
    # VWAP confirmation
    if features["vwap_deviation"] > 0.001:
        bullish_signals += 1
    elif features["vwap_deviation"] < -0.001:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features["stoch_k"] > features["stoch_d"] and features["stoch_k"] < 80:
        bullish_signals += 1
    if features["stoch_k"] < features["stoch_d"] and features["stoch_k"] > 20:
        bearish_signals += 1
    
    # MACD confirmation
    if features["macd_histogram"] > 0:
        bullish_signals += 1
    elif features["macd_histogram"] < 0:
        bearish_signals += 1
    
    # OBV slope confirmation
    if features["obv_slope"] > 0:
        bullish_signals += 1
    elif features["obv_slope"] < 0:
        bearish_signals += 1
    
    # Require 2+ confirmations matching the prediction direction
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction