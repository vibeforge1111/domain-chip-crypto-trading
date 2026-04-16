def guard(features: dict, prediction: str) -> str:
    """Filter signals by detecting true vs false compression using ATR and BB metrics."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # True compression: low volatility (low atr_ratio) + narrow bands (low bb_width)
    is_compression = atr_ratio < 0.75 and bb_width < 0.85
    
    if is_compression:
        # Skip if at extreme band position (false compression - likely to break out)
        if bb_pct_b < 0.2 or bb_pct_b > 0.8:
            return "skip"
        
        # Skip if extreme stoch reading (potential reversal during compression)
        if stoch_k < 20 or stoch_k > 80:
            return "skip"
        
        # Skip if severe VWAP deviation (compression should be balanced)
        if abs(vwap_deviation) > 0.015:
            return "skip"
    
    return prediction