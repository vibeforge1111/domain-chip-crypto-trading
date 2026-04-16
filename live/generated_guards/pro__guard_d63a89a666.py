def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    Focus: Filter based on vwap_deviation AND momentum_score disagreement
    """
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Bullish momentum but price below VWAP = disagreement
    if momentum > 0.2 and vwap_dev < -0.005:
        return "skip"
    # Bearish momentum but price above VWAP = disagreement
    if momentum < -0.2 and vwap_dev > 0.005:
        return "skip"
    
    return prediction