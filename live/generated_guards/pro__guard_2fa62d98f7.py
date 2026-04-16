def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    stoch_k = features.get("stoch_k", 50)
    macd_hist = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum alignment check
    momentum_bullish = momentum > 0 and macd_hist > 0
    momentum_bearish = momentum < 0 and macd_hist < 0
    
    # Skip if extreme VWAP deviation with momentum disagreement
    if abs(vwap_dev) > 0.015:
        if prediction == "long" and not momentum_bullish:
            return "skip"
        if prediction == "short" and not momentum_bearish:
            return "skip"
    
    # Skip if strong trend divergence between short and 2h RSI
    if prediction == "long" and rsi_2h < 35 and stoch_k < 30:
        return "skip"
    if prediction == "short" and rsi_2h > 65 and stoch_k > 70:
        return "skip"
    
    return prediction