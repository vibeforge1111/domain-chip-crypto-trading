def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like stoch_k, stoch_d, etc.
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Check for stochastic crossover timing
    crossover_delta = stoch_k - stoch_d
    
    # Long entry: stochastic crossover up in oversold zone (below 30)
    if prediction == 'long':
        if stoch_d >= 30 or crossover_delta <= 0:
            return "skip"
    
    # Short entry: stochastic crossover down in overbought zone (above 70)
    elif prediction == 'short':
        if stoch_d <= 70 or crossover_delta >= 0:
            return "skip"
    
    return prediction