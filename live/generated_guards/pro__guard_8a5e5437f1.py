def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak momentum alignment or extreme BB positions."""
    ema_slope = features.get("ema_slope", 0)
    momentum_score = features.get("momentum_score", 0)
    bb_position = features.get("bb_position", 0.5)
    volatility_regime = features.get("volatility_regime", 0.5)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Skip if trend and momentum are strongly misaligned
    trend_momentum_diff = abs(ema_slope - momentum_score)
    if trend_momentum_diff > 1.5:
        return "skip"
    
    # Skip if price is at extreme BB position (reversal risk)
    if bb_position > 0.92 or bb_position < 0.08:
        return "skip"
    
    # Skip in extremely low volatility (chop market)
    if volatility_regime < 0.2 and volume_ratio < 0.8:
        return "skip"
    
    return prediction