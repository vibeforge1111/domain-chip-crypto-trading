def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR ratio, BB width, and momentum."""
    atr_ratio = features.get('atr_ratio', 1)
    bb_width = features.get('bb_width', 1)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    obv_slope = features.get('obv_slope', 0)
    
    # True compression: both ATR and BB width are low
    is_compressed = atr_ratio < 0.75 and bb_width < 0.35
    
    if is_compressed:
        # During compression, require momentum alignment
        if prediction == 'long':
            # Reject if stochastic still bearish or RSI context weak
            if stoch_k < 30 or rsi_2h < 40:
                return 'skip'
            # Reject if OBV diverging (no volume accumulation)
            if obv_slope < 0:
                return 'skip'
        
        if prediction == 'short':
            # Reject if stochastic still bullish or RSI context strong
            if stoch_k > 70 or rsi_2h > 60:
                return 'skip'
            # Reject if OBV diverging (no volume distribution)
            if obv_slope > 0:
                return 'skip'
    
    # Stochastic not confirming direction (cross not aligned)
    if stoch_k < stoch_d and prediction == 'long':
        return 'skip'
    if stoch_k > stoch_d and prediction == 'short':
        return 'skip'
    
    return prediction