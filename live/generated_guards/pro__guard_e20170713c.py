def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation
    if features.get("rsi_14", 50) < 35:
        bullish_signals += 1
    elif features.get("rsi_14", 50) > 65:
        bearish_signals += 1
    
    # Stochastic confirmation
    if features.get("stoch_k", 50) < 20 and features.get("stoch_d", 50) < 20:
        bullish_signals += 1
    elif features.get("stoch_k", 50) > 80 and features.get("stoch_d", 50) > 80:
        bearish_signals += 1
    
    # VWAP confirmation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish_signals += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish_signals += 1
    
    # OBV slope confirmation
    if features.get("obv_slope", 0) > 0:
        bullish_signals += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_signals += 1
    
    # MACD histogram confirmation
    if features.get("macd_histogram", 0) > 0:
        bullish_signals += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_signals += 1
    
    # Bollinger Band position confirmation
    if features.get("bb_pct_b", 0.5) < 0.2:
        bullish_signals += 1
    elif features.get("bb_pct_b", 0.5) > 0.8:
        bearish_signals += 1
    
    # Require 2+ indicators to agree with direction
    if prediction == "long" and bearish_signals > 1:
        return "skip"
    if prediction == "short" and bullish_signals > 1:
        return "skip"
    
    return prediction