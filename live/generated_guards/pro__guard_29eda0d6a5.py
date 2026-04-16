def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    vwap_deviation = features.get('vwap_deviation', 0)
    momentum_score = features.get('momentum_score', 0)
    
    # Disagreement: price position vs momentum direction
    if vwap_deviation * momentum_score < -0.001:
        return 'skip'
    
    return prediction