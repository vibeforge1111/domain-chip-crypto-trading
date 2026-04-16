def guard(features: dict, prediction: str) -> str:
    """Filter trades when high volatility meets weak momentum."""
    vol_regime = features.get('volatility_regime', 0.5)
    momentum = features.get('momentum_score', 0)
    
    # Reject when high volatility but weak momentum (choppy/fading moves)
    if vol_regime > 0.7 and momentum < 0.3:
        return "skip"
    return prediction