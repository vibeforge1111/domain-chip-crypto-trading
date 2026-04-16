def guard(features: dict, prediction: str) -> str:
    """Reject trades where RSI and momentum disagree (divergence signal)."""
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    
    # Standardize both to same polarity: positive = bullish, negative = bearish
    rsi_direction = rsi - 50  # +50 to -50 range
    momentum_direction = momentum
    
    # Skip if strong divergence (signs don't match)
    if rsi_direction * momentum_direction < 0:
        return "skip"
    
    return prediction