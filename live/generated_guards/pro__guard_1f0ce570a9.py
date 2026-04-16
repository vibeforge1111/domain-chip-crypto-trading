def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject: price above VWAP but momentum diverging downward
    if vwap_dev > 0.015 and momentum < -0.25:
        return "skip"
    
    # Reject: price below VWAP but momentum diverging upward
    if vwap_dev < -0.015 and momentum > 0.25:
        return "skip"
    
    # Reject: oversold stochastic without bullish momentum support
    if prediction == "long" and stoch_k < 20 and momentum < -0.1:
        return "skip"
    
    # Reject: overbought stochastic without bearish momentum support
    if prediction == "short" and stoch_k > 80 and momentum > 0.1:
        return "skip"
    
    return prediction