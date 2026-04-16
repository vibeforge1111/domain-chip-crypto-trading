def guard(features: dict, prediction: str) -> str:
    """Filter trades when candle body is small (doji) and momentum is weak."""
    body_ratio = features.get("body_ratio", 1.0)
    momentum_score = features.get("momentum_score", 0.5)
    
    # Skip if doji-like candle (small body) AND weak momentum
    if body_ratio < 0.2 and momentum_score < 0.4:
        return "skip"
    
    return prediction