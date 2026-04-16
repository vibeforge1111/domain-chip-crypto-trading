def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    agree_count = 0
    
    # Bollinger Band position: longs want >0.5, shorts want <0.5
    if prediction == "long" and features.get("bb_pct_b", 0.5) > 0.5:
        agree_count += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) < 0.5:
        agree_count += 1
    
    # VWAP deviation: longs want >0, shorts want <0
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        agree_count += 1
    
    # Stochastic: longs want oversold (<30), shorts want overbought (>70)
    if prediction == "long" and features.get("stoch_k", 50) < 30:
        agree_count += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 70:
        agree_count += 1
    
    # OBV slope: longs want positive, shorts want negative
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        agree_count += 1
    
    # MACD histogram: longs want positive, shorts want negative
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        agree_count += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        agree_count += 1
    
    # Require at least 2 indicators to agree
    if agree_count < 2:
        return "skip"
    
    return prediction