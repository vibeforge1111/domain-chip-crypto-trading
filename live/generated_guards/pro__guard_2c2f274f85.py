def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP position and momentum."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if price far above VWAP but momentum is bearish
    if vwap_dev > 0.012 and momentum < -0.25:
        return "skip"
    # Skip if price far below VWAP but momentum is bullish
    if vwap_dev < -0.012 and momentum > 0.25:
        return "skip"
    
    return prediction