def guard(features: dict, prediction: str) -> str:
    """Filter trades when volatility is too low - avoid range-bound chop."""
    if prediction == "skip":
        return prediction
    
    atr_ratio = features.get("atr_ratio", 1.0)
    volatility_regime = features.get("volatility_regime", 0.5)
    range_pct = features.get("range_pct", 0.0)
    
    # Skip if volatility is very low (choppy market)
    if atr_ratio < 0.6 and volatility_regime < 0.3:
        return "skip"
    
    # Skip if candle range is suspiciously small
    if range_pct < 0.005:
        return "skip"
    
    return prediction