def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position extremes."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    # Only allow trades at BB extreme zones (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    return prediction