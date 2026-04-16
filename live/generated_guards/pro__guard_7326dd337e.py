def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover timing for entry precision."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Long: require bullish crossover (stoch_k crosses above stoch_d)
    if prediction == "long":
        if stoch_k <= stoch_d:
            return "skip"
        # Reject if already in overbought territory (late entry)
        if stoch_k > 85:
            return "skip"
    
    # Short: require bearish crossover (stoch_k crosses below stoch_d)
    elif prediction == "short":
        if stoch_k >= stoch_d:
            return "skip"
        # Reject if already in oversold territory (late entry)
        if stoch_k < 15:
            return "skip"
    
    return prediction