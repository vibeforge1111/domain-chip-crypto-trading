def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to avoid volatility traps."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 0.02)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: both ATR and BB narrow
    in_compression = atr_ratio < 0.85 and bb_width < 0.015
    
    # False compression trap: compressed but price at BB extreme
    at_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
    
    # Overbought/oversold in compression = likely trap
    stoch_extreme = stoch_k < 20 or stoch_k > 80
    
    # Skip if compression is actually a trap setting up
    if in_compression and at_extreme and stoch_extreme:
        return "skip"
    
    return prediction