def guard(features: dict, prediction: str) -> str:
    """Skip trades during low volatility consolidation phases."""
    bb_width = features.get('bb_width', 0)
    volatility_regime = features.get('volatility_regime', 0)
    
    # Skip if BB is tight AND volatility is low - market is choppy
    if bb_width < 0.15 and volatility_regime < 0.4:
        return 'skip'
    
    return prediction