def guard(features: dict, prediction: str) -> str:
    """Filter signals based on RSI momentum confirmation across timeframes."""
    if prediction == "skip":
        return "skip"
    
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Reject if short-term RSI diverges strongly from longer-term RSI
    if abs(rsi_14 - rsi_2h) > 20:
        return "skip"
    
    # Reject if Stochastic shows divergence from its smoothed line
    if abs(stoch_k - stoch_d) > 30:
        return "skip"
    
    return prediction