def guard(features: dict, prediction: str) -> str:
    """Only allow trades at Bollinger Band extremes (<0.05 or >0.95)."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Reject trades not at BB extremes
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        return prediction
    return "skip"