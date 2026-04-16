def guard(features: dict, prediction: str) -> str:
    """Guard using stochastic crossover timing with momentum confirmation."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    obv_slope = features.get('obv_slope', 0)
    
    if prediction == 'long':
        # Reject if no bullish crossover (k below or equal to d)
        if stoch_k <= stoch_d:
            return 'skip'
        # Reject if crossover not in oversold zone or overbought
        if stoch_k > 80 or stoch_k < 20:
            return 'skip'
        # Require price near/below VWAP and positive volume flow
        if vwap_dev > 0.005 or obv_slope < 0:
            return 'skip'
    
    elif prediction == 'short':
        # Reject if no bearish crossover (k above or equal to d)
        if stoch_k >= stoch_d:
            return 'skip'
        # Reject if crossover not in overbought zone or oversold
        if stoch_k < 20 or stoch_k > 80:
            return 'skip'
        # Require price near/above VWAP and negative volume flow
        if vwap_dev < -0.005 or obv_slope > 0:
            return 'skip'
    
    return prediction