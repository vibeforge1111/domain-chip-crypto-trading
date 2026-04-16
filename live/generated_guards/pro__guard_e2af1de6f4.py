def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    bb_pos = features.get("bb_pct_b", 0.5)
    
    # Skip if momentum contradicts VWAP position at band extremes
    if bb_pos > 0.85 and momentum < -0.2 and vwap_dev > 0.015:
        return "skip"
    if bb_pos < 0.15 and momentum > 0.2 and vwap_dev < -0.015:
        return "skip"
    
    return prediction