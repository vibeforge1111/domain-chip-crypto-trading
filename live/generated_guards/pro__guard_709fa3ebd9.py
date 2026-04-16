def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long':
        # Reject if price above VWAP but momentum bearish
        if vwap_dev > 0.003 and momentum < -0.15:
            return 'skip'
        # Reject if overbought on stochastic
        if stoch_k > 80:
            return 'skip'
    elif prediction == 'short':
        # Reject if price below VWAP but momentum bullish
        if vwap_dev < -0.003 and momentum > 0.15:
            return 'skip'
        # Reject if oversold on stochastic
        if stoch_k < 20:
            return 'skip'
    
    return prediction