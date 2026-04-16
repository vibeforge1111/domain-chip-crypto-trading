def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish = 0
    if features.get("vwap_deviation", 0) > 0:
        bullish += 1
    if features.get("stoch_k", 50) > 50 and features.get("stoch_d", 50) > 50:
        bullish += 1
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    if features.get("bb_pct_b", 0.5) > 0.5:
        bullish += 1
    if features.get("rsi_2h", 50) > 50:
        bullish += 1
    
    # Count bearish signals
    bearish = 0
    if features.get("vwap_deviation", 0) < 0:
        bearish += 1
    if features.get("stoch_k", 50) < 50 and features.get("stoch_d", 50) < 50:
        bearish += 1
    if features.get("obv_slope", 0) < 0:
        bearish += 1
    if features.get("macd_histogram", 0) < 0:
        bearish += 1
    if features.get("bb_pct_b", 0.5) < 0.5:
        bearish += 1
    if features.get("rsi_2h", 50) < 50:
        bearish += 1
    
    # Require 2+ indicators to agree with prediction direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction