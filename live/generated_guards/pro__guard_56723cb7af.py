def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish signals
    bullish = 0
    bearish = 0
    
    # RSI confirmation (not extreme)
    if features["rsi_14"] < 70:
        bullish += 1
    if features["rsi_14"] > 30:
        bearish += 1
    
    # Stochastic confirmation
    if features["stoch_k"] < 80:
        bullish += 1
    if features["stoch_k"] > 20:
        bearish += 1
    
    # VWAP deviation confirmation
    if features["vwap_deviation"] > -0.005:
        bullish += 1
    if features["vwap_deviation"] < 0.005:
        bearish += 1
    
    # OBV slope confirmation
    if features["obv_slope"] > 0:
        bullish += 1
    if features["obv_slope"] < 0:
        bearish += 1
    
    # MACD histogram confirmation
    if features["macd_histogram"] > 0:
        bullish += 1
    if features["macd_histogram"] < 0:
        bearish += 1
    
    # Require 2+ signals to agree with prediction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction