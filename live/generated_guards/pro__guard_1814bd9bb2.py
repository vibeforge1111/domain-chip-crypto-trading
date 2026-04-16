def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation contradicts momentum."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # For longs: expect positive vwap_dev AND positive momentum
        if vwap_dev < 0 and momentum < 0:
            return "skip"
        # Skip if strong bearish disagreement
        if momentum < -0.3 and vwap_dev < -0.005:
            return "skip"
        # Wide context bearish
        if rsi_2h < 35 and momentum < 0:
            return "skip"
    
    if prediction == "short":
        # For shorts: expect negative vwap_dev AND negative momentum
        if vwap_dev > 0 and momentum > 0:
            return "skip"
        # Skip if strong bullish disagreement
        if momentum > 0.3 and vwap_dev > 0.005:
            return "skip"
        # Wide context bullish
        if rsi_2h > 65 and momentum > 0:
            return "skip"
    
    return prediction