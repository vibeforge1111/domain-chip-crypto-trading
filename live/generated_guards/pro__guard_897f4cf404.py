def guard(features: dict, prediction: str) -> str:
    """Skip trades where momentum_score and vwap_deviation disagree."""
    momentum = features.get('momentum_score', 0)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Skip if bullish momentum but price far below VWAP
    if momentum > 0.25 and vwap_dev < -0.015:
        return "skip"
    
    # Skip if bearish momentum but price far above VWAP
    if momentum < -0.25 and vwap_dev > 0.015:
        return "skip"
    
    return prediction