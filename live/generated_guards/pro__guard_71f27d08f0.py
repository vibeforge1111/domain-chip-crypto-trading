def guard(features: dict, prediction: str) -> str:
    """Filter signals where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Price above VWAP but momentum bearish
    if vwap_dev > 0.003 and momentum < -0.15:
        return "skip"
    
    # Price below VWAP but momentum bullish
    if vwap_dev < -0.003 and momentum > 0.15:
        return "skip"
    
    # Stochastics disagree with momentum at extremes
    if stoch_k > 80 and momentum < -0.1:
        return "skip"
    if stoch_k < 20 and momentum > 0.1:
        return "skip"
    
    return prediction