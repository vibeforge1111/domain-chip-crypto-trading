def guard(features: dict, prediction: str) -> str:
    """Filter false compressions using BB width, ATR ratio, and position."""
    bb_width = features.get("bb_width", 1.0)
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    macd_histogram = features.get("macd_histogram", 0.0)
    
    # True compression: tight bands + rising ATR (volatility building)
    if bb_width < 0.15 and atr_ratio < 0.8:
        return "skip"
    
    # Reversal trap: extreme BB position with stoch divergence
    bb_extreme = bb_pct_b > 0.85 or bb_pct_b < 0.15
    stoch_extreme = stoch_k > 80 or stoch_k < 20
    weak_momentum = macd_histogram * (1 if bb_pct_b > 0.5 else -1) < 0
    
    if bb_extreme and stoch_extreme and weak_momentum:
        return "skip"
    
    return prediction