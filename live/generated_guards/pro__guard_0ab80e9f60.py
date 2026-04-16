def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters trades against momentum alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Reject longs when stoch_k is above stoch_d (already bullish momentum)
    if prediction == 'long' and stoch_k > stoch_d:
        return "skip"
    
    # Reject shorts when stoch_k is below stoch_d (already bearish momentum)
    if prediction == 'short' and stoch_k < stoch_d:
        return "skip"
    
    # Reject longs when deeply overbought (risky entry)
    if prediction == 'long' and stoch_k > 80:
        return "skip"
    
    # Reject shorts when deeply oversold (bounce risk)
    if prediction == 'short' and stoch_k < 20:
        return "skip"
    
    return prediction