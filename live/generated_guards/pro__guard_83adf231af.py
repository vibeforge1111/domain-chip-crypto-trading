def guard(features: dict, prediction: str) -> str:
    """Custom guard function for stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Bullish: stoch_k crosses above stoch_d in oversold territory
    if prediction == "long":
        if not (stoch_k > stoch_d and stoch_k < 30):
            return "skip"
        # Confirm wider timeframe not overbought
        if rsi_2h > 70:
            return "skip"
        # Ensure not at upper band (check for room to run)
        if bb_pct_b > 0.85:
            return "skip"
    
    # Bearish: stoch_k crosses below stoch_d in overbought territory
    elif prediction == "short":
        if not (stoch_k < stoch_d and stoch_k > 70):
            return "skip"
        # Confirm wider timeframe not oversold
        if rsi_2h < 30:
            return "skip"
        # Ensure not at lower band
        if bb_pct_b < 0.15:
            return "skip"
    
    return prediction