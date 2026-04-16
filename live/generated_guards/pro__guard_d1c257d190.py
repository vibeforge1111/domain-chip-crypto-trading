def guard(features: dict, prediction: str) -> str:
    """Guard against weak candle structures and trend disalignment."""
    # Filter out doji-like candles (small body relative to range)
    if features.get('body_ratio', 1) < 0.2:
        return "skip"
    
    # Filter out trades with excessive wicking (rejection signals)
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    if total_wick > 0.7:
        return "skip"
    
    # In low trend strength, require strong momentum confirmation
    if features.get('trend_strength', 1) < 0.3 and abs(features.get('momentum_score', 0)) < 0.4:
        return "skip"
    
    return prediction