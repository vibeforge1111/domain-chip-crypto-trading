def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip if price is too close to VWAP (within 0.2% of price)
    if abs(vwap_dev) < 0.002:
        return "skip"
    
    return prediction