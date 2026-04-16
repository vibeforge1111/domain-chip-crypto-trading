def guard(features: dict, prediction: str) -> str:
    """Guard using bb_pct_b extremes as high-confidence entry zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    
    # Only allow trades at extreme BB positions (<0.05 or >0.95)
    is_extreme_bb = bb_pct_b < 0.05 or bb_pct_b > 0.95
    
    # Reject if not at extreme BB position
    if not is_extreme_bb:
        return "skip"
    
    # Additional filter: avoid overbought/oversold exhaustion
    if prediction == "long" and rsi_14 > 75:
        return "skip"
    if prediction == "short" and rsi_14 < 25:
        return "skip"
    
    return prediction