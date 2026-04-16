def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction using OBV slope."""
    obv_slope = features.get('obv_slope', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Long trades need bullish volume flow
    if prediction == 'long' and obv_slope < 0:
        return 'skip'
    
    # Short trades need bearish volume flow
    if prediction == 'short' and obv_slope > 0:
        return 'skip'
    
    # Confirm with momentum: longs need some upside momentum
    if prediction == 'long' and stoch_k < 20:
        return 'skip'
    
    return prediction