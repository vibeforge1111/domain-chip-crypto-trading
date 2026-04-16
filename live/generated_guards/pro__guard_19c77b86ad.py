def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover quality and momentum alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if prediction contradicts crossover direction
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    # Skip if already in extreme overbought/oversold zone
    if prediction == 'long' and stoch_k > 80:
        return 'skip'
    if prediction == 'short' and stoch_k < 20:
        return 'skip'
    
    # Confirm 2h RSI aligns with prediction direction
    if prediction == 'long' and rsi_2h > 70:
        return 'skip'
    if prediction == 'short' and rsi_2h < 30:
        return 'skip'
    
    return prediction