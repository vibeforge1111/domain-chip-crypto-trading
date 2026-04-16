def guard(features: dict, prediction: str) -> str:
    """Filter trades based on VWAP deviation and momentum disagreement."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Skip if price is too far from VWAP (>2.5% deviation)
    if abs(vwap_deviation) > 0.025:
        return "skip"
    
    # Skip if momentum disagrees with prediction direction
    if prediction == "long" and momentum_score < -0.25:
        return "skip"
    if prediction == "short" and momentum_score > 0.25:
        return "skip"
    
    # Skip if stochastic is in extreme zone and conflicts with prediction
    if prediction == "long" and stoch_k > 80:
        return "skip"
    if prediction == "short" and stoch_k < 20:
        return "skip"
    
    return prediction