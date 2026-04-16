def guard(features: dict, prediction: str) -> str:
    """Filter out low-volume breakouts (high range without volume confirmation)."""
    atr_ratio = features.get("atr_ratio", 1)
    volume_ratio = features.get("volume_ratio", 1)
    
    # Reject if price moved significantly (above ATR) but without volume confirmation
    if atr_ratio > 1.3 and volume_ratio < 0.8:
        return "skip"
    
    return prediction