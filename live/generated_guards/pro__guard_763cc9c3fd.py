def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    
    bullish_signals = 0
    bearish_signals = 0
    
    # BB confirmation: below middle = bullish, above = bearish
    if bb < 0.4:
        bullish_signals += 1
    elif bb > 0.6:
        bearish_signals += 1
    
    # VWAP confirmation
    if vwap < -0.005:
        bullish_signals += 1
    elif vwap > 0.005:
        bearish_signals += 1
    
    # Stochastic confirmation
    if stoch_k < 30:
        bullish_signals += 1
    elif stoch_k > 70:
        bearish_signals += 1
    
    # RSI confirmation
    if rsi_2h < 40:
        bullish_signals += 1
    elif rsi_2h > 60:
        bearish_signals += 1
    
    # Momentum confirmation
    if obv > 0 and macd > 0:
        bullish_signals += 1
    elif obv < 0 and macd < 0:
        bearish_signals += 1
    
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction