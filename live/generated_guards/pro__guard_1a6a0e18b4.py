def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Skip if bullish momentum but price far below VWAP, or bearish momentum but price far above
    if momentum > 0.3 and vwap_dev < -0.005:
        return "skip"
    if momentum < -0.3 and vwap_dev > 0.005:
        return "skip"
    
    return prediction