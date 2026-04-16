def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum_score and vwap_deviation disagree."""
    momentum = features.get("momentum_score", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Bullish momentum but price far below VWAP → disagreement
    if momentum > 0.3 and vwap_dev < -0.005:
        return "skip"
    # Bearish momentum but price far above VWAP → disagreement
    if momentum < -0.3 and vwap_dev > 0.005:
        return "skip"
    
    return prediction