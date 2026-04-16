def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using BB width and ATR ratio."""
    bb_width = features.get("bb_width", 0.5)
    atr_ratio = features.get("atr_ratio", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    
    # False compression: tight bands but elevated volatility
    if bb_width < 0.15 and atr_ratio > 1.2:
        return "skip"
    
    # Extreme stochastic with price far from VWAP (reversal setup)
    if stoch_k > 85 and stoch_d > 80 and abs(vwap_dev) > 0.01:
        return "skip"
    
    if stoch_k < 15 and stoch_d < 20 and abs(vwap_dev) > 0.01:
        return "skip"
    
    return prediction