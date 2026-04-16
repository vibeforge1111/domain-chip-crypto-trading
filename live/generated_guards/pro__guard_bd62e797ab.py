def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Filter when vwap deviation and momentum strongly disagree
    disagreement = vwap_dev * momentum
    
    # For longs: skip if price above VWAP but bearish momentum
    if prediction == 'long' and vwap_dev > 0.008 and momentum < -0.05:
        return 'skip'
    
    # For shorts: skip if price below VWAP but bullish momentum
    if prediction == 'short' and vwap_dev < -0.008 and momentum > 0.05:
        return 'skip'
    
    return prediction