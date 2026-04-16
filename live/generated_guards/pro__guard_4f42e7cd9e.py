def guard(features: dict, prediction: str) -> str:
    """Filter trades based on stochastic crossover timing precision."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Calculate stochastic spread and crossover zone
    stoch_spread = abs(stoch_k - stoch_d)
    stoch_avg = (stoch_k + stoch_d) / 2
    
    # Reject if stochastic is in dead zone (no clear momentum)
    if 30 < stoch_avg < 70:
        return 'skip'
    
    # Reject if no meaningful spread between k and d (weak crossover)
    if stoch_spread < 5:
        return 'skip'
    
    # Confirm with wider timeframe RSI alignment
    if prediction == 'long' and rsi_2h > 60:
        return 'skip'
    if prediction == 'short' and rsi_2h < 40:
        return 'skip'
    
    return prediction