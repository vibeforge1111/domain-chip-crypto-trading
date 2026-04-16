def guard(features: dict, prediction: str) -> str:
    """Guard against momentum-volume divergence signals."""
    momentum = features.get("momentum_score", 0)
    obv = features.get("obv_slope", 0)
    range_pct = features.get("range_pct", 0)
    atr_ratio = features.get("atr_ratio", 1)
    
    # Reject if momentum and volume flow diverge
    if prediction == "long" and momentum > 0.1 and obv < -0.05:
        return "skip"
    if prediction == "short" and momentum < -0.1 and obv > 0.05:
        return "skip"
    
    # Skip low-volatility chop (range must exceed half of average ATR)
    if range_pct < atr_ratio * 0.5:
        return "skip"
    
    return prediction