def guard(features: dict, prediction: str) -> str:
    """Filter false compression breakouts using ATR, BB, and momentum."""
    bb_width = features.get("bb_width", 0)
    atr_ratio = features.get("atr_ratio", 1)
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    obv_slope = features.get("obv_slope", 0)
    
    # True compression: BB squeezed (low width) + low ATR = potential breakout
    is_compressed = bb_width < 0.3 and atr_ratio < 0.7
    
    # False breakout: compressed but no momentum confirmation
    if is_compressed:
        momentum_weak = abs(macd_histogram) < 0.0005 and abs(obv_slope) < 0.01
        stoch_neutral = 30 < stoch_k < 70
        if momentum_weak and stoch_neutral:
            return "skip"
    
    return prediction