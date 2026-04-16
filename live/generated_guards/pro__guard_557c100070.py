def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree with prediction."""
    if prediction == "skip":
        return prediction
    
    momentum = features.get("momentum_score", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip long when both indicators are bearish
    if prediction == "long" and momentum < 0 and vwap_dev < -0.001:
        return "skip"
    
    # Skip short when both indicators are bullish
    if prediction == "short" and momentum > 0 and vwap_dev > 0.001:
        return "skip"
    
    return prediction