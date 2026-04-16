def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish confirmations
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 40:
        bullish_count += 1
    elif features.get("rsi_14", 50) > 60:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 20:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 80:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # BB position confirmation
    if features.get("bb_pct_b", 0.5) < 0.2:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.8:
        bearish_count += 1
    
    # Require 2+ confirmations matching the predicted direction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction