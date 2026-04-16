def guard(features: dict, prediction: str) -> str:
    """Reject when RSI and momentum_score show strong divergence."""
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    rsi_norm = (rsi - 50) / 50  # Convert to -1 to 1 scale
    
    # Reject if RSI and momentum disagree beyond threshold
    if abs(rsi_norm - momentum) > 0.35:
        return "skip"
    return prediction