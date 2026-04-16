def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    signals_aligned = 0
    
    # RSI confirmation
    if prediction == "long" and features.get("rsi_14", 50) > 50:
        signals_aligned += 1
    elif prediction == "short" and features.get("rsi_14", 50) < 50:
        signals_aligned += 1
    
    # 2h RSI wider context confirmation
    if prediction == "long" and features.get("rsi_2h", 50) > 50:
        signals_aligned += 1
    elif prediction == "short" and features.get("rsi_2h", 50) < 50:
        signals_aligned += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features.get("vwap_deviation", 0) > 0:
        signals_aligned += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) < 0:
        signals_aligned += 1
    
    # Bollinger Band position confirmation
    if prediction == "long" and features.get("bb_pct_b", 0.5) > 0.5:
        signals_aligned += 1
    elif prediction == "short" and features.get("bb_pct_b", 0.5) < 0.5:
        signals_aligned += 1
    
    # Stochastic confirmation
    if prediction == "long" and features.get("stoch_k", 50) > 50:
        signals_aligned += 1
    elif prediction == "short" and features.get("stoch_k", 50) < 50:
        signals_aligned += 1
    
    # OBV slope confirmation
    if prediction == "long" and features.get("obv_slope", 0) > 0:
        signals_aligned += 1
    elif prediction == "short" and features.get("obv_slope", 0) < 0:
        signals_aligned += 1
    
    # MACD histogram confirmation
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        signals_aligned += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        signals_aligned += 1
    
    return prediction if signals_aligned >= 2 else "skip"