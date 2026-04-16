def guard(features: dict, prediction: str) -> str:
    """Filter signals with VWAP/momentum disagreement or conflicting new features."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Disagreement between VWAP deviation and momentum
    if vwap_dev * momentum < 0:
        return "skip"
    
    # Conflicting short-term vs medium-term momentum
    if (stoch_k > 70 and rsi_2h < 40) or (stoch_k < 30 and rsi_2h > 60):
        return "skip"
    
    return prediction