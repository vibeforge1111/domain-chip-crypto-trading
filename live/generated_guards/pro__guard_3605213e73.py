def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Filter longs when price below VWAP and momentum is bearish
    if prediction == 'long' and vwap_dev < -0.005 and momentum < 0:
        return 'skip'
    
    # Filter shorts when price above VWAP and momentum is bullish
    if prediction == 'short' and vwap_dev > 0.005 and momentum > 0:
        return 'skip'
    
    return prediction