def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip long when price far below VWAP with bearish momentum and overbought stoch
    if prediction == 'long' and vwap_dev < -0.003 and momentum < 0 and stoch_k > 70:
        return 'skip'
    
    # Skip short when price far above VWAP with bullish momentum and oversold stoch
    if prediction == 'short' and vwap_dev > 0.003 and momentum > 0 and stoch_k < 30:
        return 'skip'
    
    return prediction