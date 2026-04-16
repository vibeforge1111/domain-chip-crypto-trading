def guard(features: dict, prediction: str) -> str:
    """Filter trades with squeeze conditions or weak momentum alignment."""
    bb_width = features.get("bb_width", 0)
    atr_ratio = features.get("atr_ratio", 1)
    volume_ratio = features.get("volume_ratio", 1)
    rsi_14 = features.get("rsi_14", 50)
    momentum_score = features.get("momentum_score", 0)
    
    # Low volatility squeeze + low volume = potential fakeout
    if bb_width < 0.5 and atr_ratio < 0.8 and volume_ratio < 0.8:
        return "skip"
    
    # Weak momentum zone - skip if RSI neutral and momentum near zero
    if 40 <= rsi_14 <= 60 and abs(momentum_score) < 0.2:
        return "skip"
    
    return prediction