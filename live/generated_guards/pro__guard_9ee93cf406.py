def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == 'long':
        # Require bullish alignment and valid entry zone (oversold)
        if stoch_k < stoch_d or stoch_d > 30:
            return 'skip'
    elif prediction == 'short':
        # Require bearish alignment and valid entry zone (overbought)
        if stoch_k > stoch_d or stoch_d < 70:
            return 'skip'
    return prediction