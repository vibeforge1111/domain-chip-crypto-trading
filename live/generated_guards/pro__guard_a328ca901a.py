def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals for long
    bullish = 0
    if features.get("vwap_deviation", 0) > 0:
        bullish += 1
    if features.get("stoch_k", 50) < 70:
        bullish += 1
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    if features.get("rsi_2h", 50) < 65:
        bullish += 1
    
    # Count bearish signals for short
    bearish = 0
    if features.get("vwap_deviation", 0) < 0:
        bearish += 1
    if features.get("stoch_k", 50) > 30:
        bearish += 1
    if features.get("macd_histogram", 0) < 0:
        bearish += 1
    if features.get("rsi_2h", 50) > 35:
        bearish += 1
    
    # Require 2+ indicators to agree with direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction