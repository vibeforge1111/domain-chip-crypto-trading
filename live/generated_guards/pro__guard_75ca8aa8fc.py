def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    Detects true vs false compression using ATR ratio, BB width, and momentum indicators.
    """
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    obv_slope = features.get('obv_slope', 0)
    vwap_deviation = features.get('vwap_deviation', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # True compression: both ATR and BB are contracted
    is_compressed = atr_ratio < 0.7 and bb_width < 0.2
    
    if is_compressed:
        # False compression filter: check momentum alignment
        if prediction == 'long':
            # Reject if momentum is bearish (stoch falling, OBV negative, below VWAP)
            if stoch_k < stoch_d or obv_slope < 0 or vwap_deviation < -0.002:
                return 'skip'
        elif prediction == 'short':
            # Reject if momentum is bullish (stoch rising, OBV positive, above VWAP)
            if stoch_k > stoch_d or obv_slope > 0 or vwap_deviation > 0.002:
                return 'skip'
    
    return prediction