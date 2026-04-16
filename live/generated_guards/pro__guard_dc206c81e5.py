def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation: require 2+ signals to agree with prediction."""
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Stochastic oversold/overbought
    if features.get("stoch_k", 50) < 25:
        bullish += 1
    elif features.get("stoch_k", 50) > 75:
        bearish += 1
    
    # Bollinger Band position
    if features.get("bb_pct_b", 0.5) < 0.15:
        bullish += 1
    elif features.get("bb_pct_b", 0.5) > 0.85:
        bearish += 1
    
    # VWAP deviation
    if features.get("vwap_deviation", 0) < -0.005:
        bullish += 1
    elif features.get("vwap_deviation", 0) > 0.005:
        bearish += 1
    
    # MACD histogram direction
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # RSI 2h trend context
    if features.get("rsi_2h", 50) < 40:
        bullish += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish += 1
    
    # OBV slope (accumulation/distribution)
    if features.get("obv_slope", 0) > 0:
        bullish += 1
    elif features.get("obv_slope", 0) < 0:
        bearish += 1
    
    # Skip if <2 signals confirm the prediction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction