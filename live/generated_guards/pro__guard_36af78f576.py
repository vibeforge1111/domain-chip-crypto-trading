def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with RSI context."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Calculate crossover strength as normalized spread
    spread = stoch_k - stoch_d
    crossover_strength = spread / max(stoch_d, 1)
    
    if prediction == 'long':
        # Require bullish crossover (k above d) from oversold
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k > 35:  # Too high, not enough pullback
            return "skip"
        if rsi_2h < 40:  # Wider trend not bullish
            return "skip"
    
    elif prediction == 'short':
        # Require bearish crossover (k below d) from overbought
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_k < 65:  # Too low, not enough rally
            return "skip"
        if rsi_2h > 60:  # Wider trend not bearish
            return "skip"
    
    return prediction