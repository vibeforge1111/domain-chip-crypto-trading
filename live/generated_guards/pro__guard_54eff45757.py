def guard(features: dict, prediction: str) -> str:
    """Reject trades during false compression setups."""
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_histogram = features.get('macd_histogram', 0)
    atr_ratio = features.get('atr_ratio', 1.0)
    
    # False compression: tight bands + price mid-range + weak momentum + low volume
    compressed = bb_width < 0.8
    mid_position = 0.35 < bb_pct_b < 0.65
    weak_momentum = obv_slope < 0 and macd_histogram < 0
    low_volume = atr_ratio < 0.9
    
    if compressed and mid_position and weak_momentum and low_volume:
        return "skip"
    
    return prediction