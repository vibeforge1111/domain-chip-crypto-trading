def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only trade at BB extremes (<5% or >95%)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction