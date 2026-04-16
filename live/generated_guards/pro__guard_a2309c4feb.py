def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject longs when price extended above VWAP but momentum contradicts (weak upside)
    if prediction == 'long' and vwap_dev > 0.008 and momentum < 0:
        return 'skip'
    
    # Reject shorts when price dropped below VWAP but momentum contradicts (weak downside)
    if prediction == 'short' and vwap_dev < -0.008 and momentum > 0:
        return 'skip'
    
    return prediction