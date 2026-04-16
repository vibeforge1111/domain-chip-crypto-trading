def guard(features: dict, prediction: str) -> str:
    """Filter trades by detecting true vs false compression patterns."""
    bb_width = features.get('bb_width', 1)
    atr_ratio = features.get('atr_ratio', 1)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: tight BB with building volatility
    is_compressed = bb_width < 0.15
    
    if is_compressed:
        # False compression: tight bands but no energy building
        if atr_ratio < 0.7:
            return "skip"
        
        # Extreme BB position during compression (reversal risk)
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            return "skip"
    
    # Extended from VWAP with weak 2h RSI context
    if abs(vwap_deviation) > 0.02 and rsi_2h < 35:
        return "skip"
    
    return prediction