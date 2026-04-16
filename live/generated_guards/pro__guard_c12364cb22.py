def guard(features: dict, prediction: str) -> str:
    """Skip trades when price is too close to VWAP with weak momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    macd = features.get('macd_histogram', 0)
    
    # If price near fair value AND momentum is weak, skip
    if abs(vwap_dev) < 0.003 and abs(macd) < 0.00005:
        return "skip"
    
    return prediction