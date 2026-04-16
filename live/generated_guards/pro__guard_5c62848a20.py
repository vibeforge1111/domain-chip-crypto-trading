def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    rsi = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_dev = features.get("vwap_deviation", 0)
    macd = features.get("macd_histogram", 0)
    obv = features.get("obv_slope", 0)
    
    bullish_count = 0
    
    # RSI alignment: both timeframes agree
    if prediction == "long" and rsi > 50 and rsi_2h > 50:
        bullish_count += 1
    elif prediction == "short" and rsi < 50 and rsi_2h < 50:
        bullish_count += 1
    
    # Stochastic alignment
    if prediction == "long" and stoch_k > 50 and stoch_d > 50:
        bullish_count += 1
    elif prediction == "short" and stoch_k < 50 and stoch_d < 50:
        bullish_count += 1
    
    # VWAP and BB position alignment
    if prediction == "long" and vwap_dev > 0 and bb_pct_b > 0.5:
        bullish_count += 1
    elif prediction == "short" and vwap_dev < 0 and bb_pct_b < 0.5:
        bullish_count += 1
    
    # Momentum alignment
    if prediction == "long" and macd > 0 and obv > 0:
        bullish_count += 1
    elif prediction == "short" and macd < 0 and obv < 0:
        bullish_count += 1
    
    return "skip" if bullish_count < 2 else prediction