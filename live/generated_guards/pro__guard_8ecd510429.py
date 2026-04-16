def guard(features: dict, prediction: str) -> str:
    """Reject trades not at Bollinger Band extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Long only at lower band extremes (<0.05) with some buffer for valid signals
    if prediction == "long" and bb_pct_b > 0.15:
        return "skip"
    
    # Short only at upper band extremes (>0.95) with buffer
    if prediction == "short" and bb_pct_b < 0.85:
        return "skip"
    
    return prediction