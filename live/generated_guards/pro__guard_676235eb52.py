def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones with RSI confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # High-confidence entry zones: bb_pct_b extremes
    in_lower_extreme = bb_pct_b < 0.05
    in_upper_extreme = bb_pct_b > 0.95
    
    # For longs: require lower band extreme AND oversold RSI AND below VWAP
    if prediction == 'long':
        if not (in_lower_extreme and rsi_14 < 35 and vwap_deviation < 0):
            return 'skip'
    
    # For shorts: require upper band extreme AND overbought RSI AND above VWAP
    elif prediction == 'short':
        if not (in_upper_extreme and rsi_14 > 65 and vwap_deviation > 0):
            return 'skip'
    
    return prediction