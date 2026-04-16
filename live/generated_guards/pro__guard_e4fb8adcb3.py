def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if price above VWAP but momentum is bearish, or price below VWAP but momentum is bullish
    if (vwap_dev > 0.005 and momentum < -0.2) or (vwap_dev < -0.005 and momentum > 0.2):
        return "skip"
    
    return prediction