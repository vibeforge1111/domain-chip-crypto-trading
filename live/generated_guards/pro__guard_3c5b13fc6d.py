def guard(features: dict, prediction: str) -> str:
    """Skip trades against OBV volume flow direction."""
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when OBV declining and stochastic oversold (weak)
    if prediction == 'long' and obv_slope < -0.5 and stoch_k < 30:
        return 'skip'
    
    # Skip shorts when OBV rising and stochastic overbought (weak)
    if prediction == 'short' and obv_slope > 0.5 and stoch_k > 70:
        return 'skip'
    
    return prediction