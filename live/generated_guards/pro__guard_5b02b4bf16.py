def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Stochastic confirmation
    if features["stoch_k"] < 20:
        bullish += 1
    elif features["stoch_k"] > 80:
        bearish += 1
    
    # VWAP confirmation
    if features["vwap_deviation"] > 0.005:
        bullish += 1
    elif features["vwap_deviation"] < -0.005:
        bearish += 1
    
    # MACD confirmation
    if features["macd_histogram"] > 0:
        bullish += 1
    elif features["macd_histogram"] < 0:
        bearish += 1
    
    # Bollinger Band position confirmation
    if features["bb_pct_b"] < 0.25:
        bullish += 1
    elif features["bb_pct_b"] > 0.75:
        bearish += 1
    
    # Require 2+ confirming signals
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction