def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    if prediction == 'long':
        # Skip if price extended above VWAP but momentum is bearish
        if vwap_dev > 0.003 and momentum < -0.1:
            return 'skip'
    elif prediction == 'short':
        # Skip if price extended below VWAP but momentum is bullish
        if vwap_dev < -0.003 and momentum > 0.1:
            return 'skip'
    return prediction