def guard(features: dict, prediction: str) -> str:
    """Only allow trades at Bollinger Band extremes as high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    if bb_pct_b > 0.05 and bb_pct_b < 0.95:
        return "skip"
    
    return prediction