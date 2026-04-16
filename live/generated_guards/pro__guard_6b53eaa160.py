def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # RSI confirmation (not overbought = bullish, not oversold = bearish)
    if features.get("rsi_14", 50) < 65:
        bullish_signals += 1
    if features.get("rsi_14", 50) > 35:
        bearish_signals += 1
    
    # VWAP confirmation (above VWAP = bullish)
    if features.get("vwap_deviation", 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Stochastic confirmation (oversold = bullish, overbought = bearish)
    if features.get("stoch_k", 50) < 30:
        bullish_signals += 1
    if features.get("stoch_k", 50) > 70:
        bearish_signals += 1
    
    # MACD histogram confirmation (positive = bullish)
    if features.get("macd_histogram", 0) > 0:
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction