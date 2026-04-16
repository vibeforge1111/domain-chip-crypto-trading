def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if price far from VWAP but momentum disagrees
    if vwap_dev > 0.01 and momentum < -0.2:
        return "skip"
    if vwap_dev < -0.01 and momentum > 0.2:
        return "skip"
    
    # Skip if bullish but stochastic overbought with high vwap deviation
    if momentum > 0.2 and stoch_k > 80 and vwap_dev > 0.008:
        return "skip"
    
    # Skip if bearish but stochastic oversold with low vwap deviation
    if momentum < -0.2 and stoch_k < 20 and vwap_dev < -0.008:
        return "skip"
    
    return prediction