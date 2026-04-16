def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Bullish timing: stoch_k crosses above stoch_d in oversold zone
    bullish_crossover = stoch_k > stoch_d and stoch_k < 30 and stoch_d < 30
    
    # Bearish timing: stoch_k crosses below stoch_d in overbought zone
    bearish_crossover = stoch_k < stoch_d and stoch_k > 70 and stoch_d > 70
    
    # Check if we have proper crossover timing for the prediction direction
    if prediction == "long" and not bullish_crossover:
        return "skip"
    if prediction == "short" and not bearish_crossover:
        return "skip"
    
    return prediction