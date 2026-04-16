def guard(features: dict, prediction: str) -> str:
    """Guard against momentum exhaustion using macd_histogram and overbought/oversold conditions."""
    macd = features.get("macd_histogram", 0)
    stoch = features.get("stoch_k", 50)
    bb_pos = features.get("bb_pct_b", 0.5)
    rsi = features.get("rsi_14", 50)
    
    # Momentum deceleration check - macd histogram near zero suggests weakening momentum
    momentum_flat = abs(macd) < 0.0003
    
    if prediction == "long":
        # Skip longs when momentum weakening + overbought + upper BB
        if momentum_flat and stoch > 75 and bb_pos > 0.85:
            return "skip"
        # Skip longs when macd turning down from positive with RSI divergence
        if macd < 0 and rsi > 65 and bb_pos > 0.8:
            return "skip"
            
    elif prediction == "short":
        # Skip shorts when momentum weakening + oversold + lower BB
        if momentum_flat and stoch < 25 and bb_pos < 0.15:
            return "skip"
        # Skip shorts when macd turning up from negative with RSI divergence
        if macd > 0 and rsi < 35 and bb_pos < 0.2:
            return "skip"
    
    return prediction