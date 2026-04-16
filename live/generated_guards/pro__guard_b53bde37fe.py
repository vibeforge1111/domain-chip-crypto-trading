def guard(features: dict, prediction: str) -> str:
    """Skip trades with VWAP deviation and momentum disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip long: price extended above VWAP but momentum weakening
    if prediction == "long" and vwap_dev > 0.012 and momentum < -0.1 and stoch_k > 75:
        return "skip"
    
    # Skip short: price extended below VWAP but momentum strengthening
    if prediction == "short" and vwap_dev < -0.012 and momentum > 0.1 and rsi_2h > 55:
        return "skip"
    
    return prediction