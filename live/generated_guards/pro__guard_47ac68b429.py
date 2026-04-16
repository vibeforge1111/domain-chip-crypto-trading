def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'long':
        # Require bullish crossover with D in oversold zone
        if stoch_k <= stoch_d or stoch_d >= 30:
            return "skip"
        # Reject if price too far above VWAP
        if vwap_dev > 0.01:
            return "skip"
    
    elif prediction == 'short':
        # Require bearish crossover with D in overbought zone
        if stoch_k >= stoch_d or stoch_d <= 70:
            return "skip"
        # Reject if price too far below VWAP
        if vwap_dev < -0.01:
            return "skip"
    
    return prediction