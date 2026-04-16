def guard(features: dict, prediction: str) -> str:
    """Skip trades that contradict the broader 2-hour trend."""
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Align with broader trend: longs need bullish 2h context, shorts need bearish
    if prediction == 'long' and rsi_2h < 50:
        return 'skip'
    if prediction == 'short' and rsi_2h > 50:
        return 'skip'
    
    # Secondary filter: confirm with VWAP alignment
    if prediction == 'long' and vwap_deviation < -0.005:
        return 'skip'
    if prediction == 'short' and vwap_deviation > 0.005:
        return 'skip'
    
    return prediction