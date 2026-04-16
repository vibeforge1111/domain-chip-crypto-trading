def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    confirmation_count = 0
    
    # Stochastics not overbought/oversold
    if 20 < features.get("stoch_k", 50) < 80 and 20 < features.get("stoch_d", 50) < 80:
        confirmation_count += 1
    
    # VWAP not too far from price
    if -0.015 < features.get("vwap_deviation", 0) < 0.01:
        confirmation_count += 1
    
    # OBV showing accumulation/distribution
    if features.get("obv_slope", 0) > 0:
        confirmation_count += 1
    
    # MACD histogram aligned with prediction
    if prediction == "long" and features.get("macd_histogram", 0) > 0:
        confirmation_count += 1
    elif prediction == "short" and features.get("macd_histogram", 0) < 0:
        confirmation_count += 1
    
    # BB position in middle range
    if 0.2 < features.get("bb_pct_b", 0.5) < 0.8:
        confirmation_count += 1
    
    # 2-hour RSI confirming direction
    if prediction == "long" and features.get("rsi_2h", 50) < 70:
        confirmation_count += 1
    elif prediction == "short" and features.get("rsi_2h", 50) > 30:
        confirmation_count += 1
    
    return prediction if confirmation_count >= 2 else "skip"