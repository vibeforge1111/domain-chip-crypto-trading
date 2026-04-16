def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum_score disagrees with vwap_deviation."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    
    # Bullish momentum but price significantly below VWAP = disagreement
    if momentum > 0.3 and vwap_dev < -0.01:
        return "skip"
    # Bearish momentum but price significantly above VWAP = disagreement
    if momentum < -0.3 and vwap_dev > 0.01:
        return "skip"
    
    return prediction