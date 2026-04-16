def guard(features: dict, prediction: str) -> str:
    """Filter trades during false compression setups."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Detect compression: low ATR + narrow BB
    is_compression = atr_ratio < 0.75 and bb_width < 0.6
    
    # False compression at extreme BB with extreme stoch = skip
    if is_compression and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    if is_compression and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    return prediction