def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extreme positions as high-confidence entry zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    trend_strength = features.get("trend_strength", 0)
    
    # Only allow trades at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Require trend alignment with BB position
    if bb_pct_b < 0.05 and trend_strength > -0.2:
        return "skip"
    if bb_pct_b > 0.95 and trend_strength < 0.2:
        return "skip"
    
    return prediction