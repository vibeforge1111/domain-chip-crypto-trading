def guard(features: dict, prediction: str) -> str:
    """Filter trades when VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Disagreement: price far above VWAP but momentum weak, or price far below VWAP but momentum strong
    above_vwap = vwap_dev > 0.01
    below_vwap = vwap_dev < -0.01
    weak_momentum = momentum < 0.25
    strong_momentum = momentum > 0.25
    
    if (above_vwap and weak_momentum) or (below_vwap and strong_momentum):
        return "skip"
    
    return prediction