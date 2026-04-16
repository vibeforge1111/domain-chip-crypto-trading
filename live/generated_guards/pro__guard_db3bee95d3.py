def guard(features: dict, prediction: str) -> str:
    """Filter trades where momentum fires in high volatility with weak volume (likely false signal)."""
    high_vol = features.get("volatility_regime", 0) > 0.6
    weak_vol = features.get("volume_ratio", 1) < 0.9
    momentum_signal = features.get("momentum_score", 0) > 0.5
    
    if high_vol and weak_vol and momentum_signal:
        return "skip"
    
    return prediction