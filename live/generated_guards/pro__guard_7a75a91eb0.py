def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing and zone confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    # Stochastic crossover timing for longs
    if prediction == "long":
        # Require bullish crossover (k above d) in valid zone
        if stoch_k <= stoch_d:
            return "skip"
        # Avoid entries in overbought territory (weak upside momentum)
        if stoch_k > 85:
            return "skip"
        # Require some bullish confirmation with d in lower half
        if stoch_d > 50:
            return "skip"
    
    # Stochastic crossover timing for shorts
    elif prediction == "short":
        # Require bearish crossover (k below d) in valid zone
        if stoch_k >= stoch_d:
            return "skip"
        # Avoid entries in oversold territory (weak downside momentum)
        if stoch_k < 15:
            return "skip"
        # Require some bearish confirmation with d in upper half
        if stoch_d < 50:
            return "skip"
    
    return prediction