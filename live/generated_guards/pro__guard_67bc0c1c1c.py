def guard(features: dict, prediction: str) -> str:
    """Filter false compression setups using BB width, ATR ratio, VWAP and stochastic."""
    bb_width = features.get("bb_width", 0.5)
    atr_ratio = features.get("atr_ratio", 1.0)
    vwap_deviation = features.get("vwap_deviation", 0.0)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: tight BB + moderate ATR + price near VWAP + balanced stochastic
    if bb_width < 0.2 and atr_ratio < 0.6:
        if abs(vwap_deviation) > 0.008 or stoch_k > 82 or stoch_k < 18:
            return "skip"
    return prediction