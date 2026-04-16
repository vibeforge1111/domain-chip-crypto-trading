def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree strongly."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Strong disagreement: price below VWAP but momentum bullish, or vice versa
    if (vwap_dev < -0.01 and momentum > 0.3) or (vwap_dev > 0.01 and momentum < -0.3):
        return "skip"
    
    return prediction