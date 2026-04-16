def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    # Count bullish signals
    bullish_count = 0
    bearish_count = 0
    
    # VWAP deviation check
    if features.get("vwap_deviation", 0) > 0.002:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.002:
        bearish_count += 1
    
    # Stochastic overbought/oversold check
    stoch_k = features.get("stoch_k", 50)
    if stoch_k < 70 and stoch_k > 30:
        if stoch_k < 50:
            bullish_count += 1
        else:
            bearish_count += 1
    
    # MACD histogram direction
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # OBV slope direction
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # RSI 2h context
    rsi_2h = features.get("rsi_2h", 50)
    if rsi_2h < 65 and rsi_2h > 35:
        if prediction == "long":
            bullish_count += 1
        else:
            bearish_count += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction