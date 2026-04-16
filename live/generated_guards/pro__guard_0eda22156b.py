def guard(features: dict, prediction: str) -> str:
    """Filter trades showing volume absorption with momentum exhaustion."""
    vol_ratio = features.get('volume_ratio', 1)
    atr_ratio = features.get('atr_ratio', 1)
    range_pct = features.get('range_pct', 0.5)
    rsi = features.get('rsi_14', 50)
    bb_position = features.get('bb_position', 0.5)
    
    # Absorption: high volume but low price movement relative to ATR
    is_absorption = vol_ratio > 1.4 and atr_ratio > 1.1 and range_pct < 0.4
    
    # Price at extreme BB position indicating potential reversal zone
    at_extreme = bb_position > 0.85 or bb_position < 0.15
    
    # Momentum exhaustion: RSI in reversal territory
    is_exhausted = rsi > 68 or rsi < 32
    
    # Skip if absorption pattern at extremes with exhausted momentum
    if is_absorption and at_extreme and is_exhausted:
        return "skip"
    
    return prediction