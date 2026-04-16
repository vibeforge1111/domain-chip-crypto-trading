def guard(features: dict, prediction: str) -> str:
    """Filter trades with wick imbalance and poor candle structure."""
    # High combined wick dominance (>0.55) indicates rejection candles
    wick_dominance = features.get('upper_wick_ratio', 0) + features.get('lower_wick_ratio', 0)
    body_ratio = features.get('body_ratio', 1)
    
    if wick_dominance > 0.55 and body_ratio < 0.35:
        return "skip"
    
    # Extreme BB position with weak momentum suggests exhaustion
    bb_position = features.get('bb_position', 0.5)
    momentum_score = features.get('momentum_score', 0)
    
    if bb_position > 0.92 and momentum_score < -0.1:
        return "skip"
    
    if bb_position < 0.08 and momentum_score > 0.1:
        return "skip"
    
    return prediction