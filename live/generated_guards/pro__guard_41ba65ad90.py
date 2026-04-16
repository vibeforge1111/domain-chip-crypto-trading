def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value with momentum confirmation."""
    vwap_dev = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip if price is too close to fair value (< 0.2% deviation)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    # Skip longs when overbought on 2h RSI and stochastic
    if prediction == "long" and rsi_2h > 70 and stoch_k > 75:
        return "skip"
    
    # Skip shorts when oversold on 2h RSI and stochastic
    if prediction == "short" and rsi_2h < 30 and stoch_k < 25:
        return "skip"
    
    return prediction