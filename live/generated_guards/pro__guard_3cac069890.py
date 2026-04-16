def guard(features: dict, prediction: str) -> str:
    """Skip if price is far from VWAP but momentum disagrees with direction."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0.5)
    
    # If price >1% away from VWAP and momentum contradicts prediction
    if abs(vwap_dev) > 0.01:
        if prediction == "long" and momentum < 0.45:
            return "skip"
        if prediction == "short" and momentum > 0.55:
            return "skip"
    
    return prediction