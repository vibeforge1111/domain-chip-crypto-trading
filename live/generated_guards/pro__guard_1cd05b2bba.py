def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, bb_pct_b, and momentum."""
    bb_width = features.get('bb_width', 0.1)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    macd_histogram = features.get('macd_histogram', 0)
    
    # True compression: low bb_width + low atr_ratio
    is_compressed = bb_width < 0.025 and atr_ratio < 0.8
    at_bb_extreme = bb_pct_b < 0.15 or bb_pct_b > 0.85
    conflicting_momentum = (stoch_k > 80 and macd_histogram < 0) or (stoch_k < 20 and macd_histogram > 0)
    
    # Skip if compressed but likely false signal (extreme position + bad momentum alignment)
    if is_compressed and at_bb_extreme and conflicting_momentum:
        return "skip"
    
    return prediction