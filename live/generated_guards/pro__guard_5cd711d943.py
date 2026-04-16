def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum-volume divergence in high volatility."""
    volume_ratio = features.get('volume_ratio', 1)
    momentum_score = features.get('momentum_score', 0)
    volatility_regime = features.get('volatility_regime', 0)
    atr_ratio = features.get('atr_ratio', 1)
    
    # High volatility but weak volume with momentum suggests unstable move
    high_volatility = volatility_regime > 0.6 or atr_ratio > 1.3
    weak_volume = volume_ratio < 0.7
    divergent_momentum = abs(momentum_score) < 0.3
    
    if high_volatility and weak_volume and divergent_momentum:
        return "skip"
    return prediction