def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Long: price above VWAP but bearish momentum OR overbought stoch
    if prediction == 'long':
        if vwap_dev > 0.01 and momentum < -0.1:
            return 'skip'
        if stoch_k > 85:
            return 'skip'
    
    # Short: price below VWAP but bullish momentum OR oversold stoch
    if prediction == 'short':
        if vwap_dev < -0.01 and momentum > 0.1:
            return 'skip'
        if stoch_k < 15:
            return 'skip'
    
    return prediction