def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and new features."""
    # True compression: both low volatility AND tight bands
    true_compression = features.get('atr_ratio', 1) < 0.8 and features.get('bb_width', 0.5) < 0.35
    
    if true_compression:
        # False breakout signals when price at extreme BB position
        bb_extreme = features.get('bb_pct_b', 0.5) < 0.2 or features.get('bb_pct_b', 0.5) > 0.8
        # Or far from VWAP in compression (distribution)
        vwap_far = abs(features.get('vwap_deviation', 0)) > 0.008
        # Or stochastics at extremes suggesting reversal
        stoch_extreme = features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15
        
        if bb_extreme or vwap_far or stoch_extreme:
            return "skip"
    
    return prediction