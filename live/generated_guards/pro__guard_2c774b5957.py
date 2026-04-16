def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.
    Uses bb_pct_b extremes (<0.05 or >0.95) as high-confidence entry zones.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction