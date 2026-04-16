def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover alignment."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Stochastic crossover must align with prediction direction
    if prediction == 'long' and stoch_k <= stoch_d:
        return 'skip'
    if prediction == 'short' and stoch_k >= stoch_d:
        return 'skip'
    
    # Require meaningful crossover strength to avoid weak signals
    if prediction == 'long' and (stoch_k - stoch_d) < 5:
        return 'skip'
    if prediction == 'short' and (stoch_d - stoch_k) < 5:
        return 'skip'
    
    # Align with 2h RSI momentum context
    if prediction == 'long' and rsi_2h < 30:
        return 'skip'
    if prediction == 'short' and rsi_2h > 70:
        return 'skip'
    
    # Validate entry location within Bollinger Bands
    if prediction == 'long' and bb_pct_b < 0.15:
        return 'skip'
    if prediction == 'short' and bb_pct_b > 0.85:
        return 'skip'
    
    return prediction