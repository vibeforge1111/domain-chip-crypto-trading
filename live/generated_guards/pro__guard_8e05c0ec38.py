def guard(features: dict, prediction: str) -> str:
    """Filter trades with vwap_deviation and momentum_score disagreement."""
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    
    # Skip if signs disagree between VWAP position and momentum direction
    if vwap_dev * momentum < 0:
        return "skip"
    
    return prediction