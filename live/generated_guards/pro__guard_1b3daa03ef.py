def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum shows deceleration via MACD histogram."""
    if prediction == "skip":
        return prediction
    
    macd_hist = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Momentum deceleration: negative or near-zero MACD histogram
    if macd_hist < 0.0005:
        # For longs: skip if momentum fading and stochastic confirmation
        if prediction == "long" and stoch_k > 70:
            return "skip"
        # For shorts: skip if momentum fading upward
        if prediction == "short" and macd_hist < 0 and stoch_k < 30:
            return "skip"
    
    # Wider context RSI divergence check
    if prediction == "long" and rsi_2h > 70 and macd_hist < 0:
        return "skip"
    if prediction == "short" and rsi_2h < 30 and macd_hist > 0:
        return "skip"
    
    return prediction