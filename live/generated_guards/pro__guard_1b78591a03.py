def guard(features: dict, prediction: str) -> str:
    """Filter trades to only extreme BB positions (high-confidence entry zones)."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    # Only allow trades at extreme BB positions
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        return prediction
    return "skip"