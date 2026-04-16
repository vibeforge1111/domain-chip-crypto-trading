def guard(features: dict, prediction: str) -> str:
    """Filter false breakouts during compression by checking momentum divergence."""
    bb_width = features.get('bb_width', 1.0)
    is_compression = bb_width < 0.25
    extreme_vwap = abs(features.get('vwap_deviation', 0)) > 0.015
    stoch_exhausted = features.get('stoch_k', 50) > 85 or features.get('stoch_k', 50) < 15
    
    # Skip false breakouts: compression with momentum divergence
    if is_compression and (extreme_vwap or stoch_exhausted):
        return "skip"
    
    return prediction