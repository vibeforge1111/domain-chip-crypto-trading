def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and bb_pct_b."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # True compression: low volatility + narrow bands
    compression = atr_ratio < 0.75 and bb_width < 0.012
    
    if compression:
        # False compression: price at extremes of BB
        if bb_pct_b < 0.15 or bb_pct_b > 0.85:
            return "skip"
        # Weak momentum: extreme stochastic within compression
        if stoch_k < 20 or stoch_k > 80:
            return "skip"
    
    return prediction