def guard(features: dict, prediction: str) -> str:
    """Filter trades in low-momentum, low-volume environments."""
    vol_regime = features.get('volatility_regime', 0.5)
    momentum = features.get('momentum_score', 0.5)
    vol_ratio = features.get('volume_ratio', 1.0)
    
    # Reject if: moderate volatility + weak momentum + low volume (choppy market)
    if 0.3 < vol_regime < 0.6 and momentum < 0.4 and vol_ratio < 0.8:
        return "skip"
    
    return prediction