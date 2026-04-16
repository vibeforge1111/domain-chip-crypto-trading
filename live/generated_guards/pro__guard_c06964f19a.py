def guard(features: dict, prediction: str) -> str:
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    bb_pos = features.get('bb_pct_b', 0.5)
    
    if prediction == 'long':
        # Long only if: bearish crossover (k below d) in oversold + price below VWAP
        if stoch_k < stoch_d and stoch_k < 35 and vwap_dev < 0:
            return prediction
        return 'skip'
    elif prediction == 'short':
        # Short only if: bullish crossover (k above d) in overbought + price above VWAP
        if stoch_k > stoch_d and stoch_k > 65 and vwap_dev > 0:
            return prediction
        return 'skip'
    return prediction