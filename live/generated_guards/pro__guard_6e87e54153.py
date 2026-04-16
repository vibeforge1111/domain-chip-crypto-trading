def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only allow entries at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        return prediction
    
    return "skip"