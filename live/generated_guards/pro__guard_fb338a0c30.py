def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP fair value with confirming BB position."""
    vwap_dev = features.get("vwap_deviation", 0)
    bb_pct = features.get("bb_pct_b", 0.5)
    # Skip if too close to VWAP (<0.2%) and mid-range on BB (0.35-0.65)
    if abs(vwap_dev) < 0.002 and 0.35 < bb_pct < 0.65:
        return "skip"
    return prediction