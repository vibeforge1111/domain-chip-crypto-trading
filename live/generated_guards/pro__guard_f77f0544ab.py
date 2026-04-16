def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if strong VWAP-momentum disagreement
    if vwap_dev > 0.015 and momentum < -0.25:
        return "skip"
    if vwap_dev < -0.015 and momentum > 0.25:
        return "skip"
    
    # Skip if stochastic diverges from Bollinger position
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    if stoch_k > 75 and bb_pct_b < 0.25:
        return "skip"
    if stoch_k < 25 and bb_pct_b > 0.75:
        return "skip"
    
    return prediction