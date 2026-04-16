def guard(features: dict, prediction: str) -> str:
    """Filter trades using compression detection (atr_ratio + bb_width)."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    macd_histogram = features.get('macd_histogram', 0)
    
    # True compression: low volatility AND tight bands
    compression = atr_ratio < 0.75 and bb_width < 0.75
    
    if compression:
        # False compression: stochastic at extremes signals reversal coming
        if stoch_k < 20 or stoch_k > 80:
            return "skip"
        
        # False compression: bb_pct_b at extremes means trend, not compression
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            return "skip"
        
        # False compression: macd histogram building means momentum present
        if abs(macd_histogram) > 0.001:
            return "skip"
    
    return prediction