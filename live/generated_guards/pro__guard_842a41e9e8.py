def guard(features: dict, prediction: str) -> str:
    """Filters signals with RSI-momentum divergence or weak volume confirmation."""
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    volume = features.get("volume_ratio", 1)
    
    # Skip if RSI extreme but momentum doesn't confirm direction
    if (rsi > 65 and momentum < -0.1) or (rsi < 35 and momentum > 0.1):
        return "skip"
    
    # Skip if low volume on strong move indication
    if abs(momentum) > 0.5 and volume < 0.8:
        return "skip"
    
    return prediction