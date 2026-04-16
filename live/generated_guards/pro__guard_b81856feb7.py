def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extremes as high-confidence entry zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow entries at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction