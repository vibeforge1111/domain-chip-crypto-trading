def guard(features: dict, prediction: str) -> str:
    """Custom guard function using bb_pct_b extremes as high-confidence entry zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only accept trades at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction