def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard for precise entries."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long signals need bullish alignment: stoch_k >= stoch_d in oversold
    if prediction == 'long':
        if stoch_k < stoch_d and stoch_k < 30:
            return "skip"
        # Additional confirmation: reject if 2h RSI contradicts
        if rsi_2h < 35:
            return "skip"
    
    # Short signals need bearish alignment: stoch_k <= stoch_d in overbought
    elif prediction == 'short':
        if stoch_k > stoch_d and stoch_k > 70:
            return "skip"
        # Additional confirmation: reject if 2h RSI contradicts
        if rsi_2h > 65:
            return "skip"
    
    return prediction