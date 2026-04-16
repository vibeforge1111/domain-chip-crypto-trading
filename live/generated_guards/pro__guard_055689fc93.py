def guard(features: dict, prediction: str) -> str:
    """Only allow trades at Bollinger Band extremes with VWAP alignment."""
    if prediction == "skip":
        return "skip"
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    
    # High-confidence entry only at BB extremes
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Confirm with VWAP alignment
    if prediction == "long" and vwap_deviation < 0:
        return prediction
    if prediction == "short" and vwap_deviation > 0:
        return prediction
    
    return "skip"