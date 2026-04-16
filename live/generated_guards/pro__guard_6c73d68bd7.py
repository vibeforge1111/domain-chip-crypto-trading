def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering using VWAP deviation."""
    vwap_dev = features.get("vwap_deviation", 0)
    
    # Skip trades when price is too close to fair value (VWAP)
    # Filter if deviation is within ±0.2% of price
    if -0.002 < vwap_dev < 0.002:
        return "skip"
    
    return prediction