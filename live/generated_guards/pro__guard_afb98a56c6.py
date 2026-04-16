def guard(features: dict, prediction: str) -> str:
    """Filter signals with conflicting RSI and momentum indicators."""
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0.5)
    
    # Reject if RSI and momentum are strongly misaligned
    rsi_extreme = rsi > 70 or rsi < 30
    momentum_weak = abs(momentum) < 0.2
    
    if rsi_extreme and momentum_weak:
        return "skip"
    return prediction