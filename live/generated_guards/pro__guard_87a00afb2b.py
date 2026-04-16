def guard(features: dict, prediction: str) -> str:
    """Reject trades when not at Bollinger Band extremes (high-confidence zones)."""
    bb = features.get("bb_pct_b", 0.5)
    # Only allow entries at BB extremes (<0.05 or >0.95)
    if bb >= 0.05 and bb <= 0.95:
        return "skip"
    return prediction