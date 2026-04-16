def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    spread = stoch_k - stoch_d
    
    if prediction == 'long':
        # Bullish crossover (k crosses above d) in oversold zone
        if spread > 3 and stoch_k < 20:
            return prediction
        return 'skip'
    
    if prediction == 'short':
        # Bearish crossover (k crosses below d) in overbought zone
        if spread < -3 and stoch_k > 80:
            return prediction
        return 'skip'
    
    return prediction