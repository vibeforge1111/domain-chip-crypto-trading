def guard(features: dict, prediction: str) -> str:
    """Filter trades at BB extremes with contracting volatility or weak volume confirmation."""
    bb_pos = features.get('bb_position', 0.5)
    atr_r = features.get('atr_ratio', 1.0)
    vol_r = features.get('volume_ratio', 1.0)
    
    # At BB extremes but ATR compressing - likely reversal trap
    if (bb_pos > 0.92 or bb_pos < 0.08) and atr_r < 0.75:
        return "skip"
    
    # Very low volume without strong range - weak conviction signal
    if vol_r < 0.5 and features.get('range_pct', 0) < 0.3:
        return "skip"
    
    return prediction