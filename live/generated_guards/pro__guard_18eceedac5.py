def guard(features: dict, prediction: str) -> str:
    """Filter trades based on wick dominance and BB squeeze interaction."""
    # Skip if candle is wick-dominated (uncertainty/indecision)
    total_wick = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    body = features.get('body_ratio', 0)
    
    if body > 0 and total_wick / body > 1.5:
        return "skip"
    
    # Skip if BB squeeze forming AND low momentum (consolidation trap)
    bb_width = features.get('bb_width', 1)
    volatility_regime = features.get('volatility_regime', 1)
    momentum = features.get('momentum_score', 0)
    
    if bb_width < 0.7 * volatility_regime and abs(momentum) < 0.3:
        return "skip"
    
    return prediction