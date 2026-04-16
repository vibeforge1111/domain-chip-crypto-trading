def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI-BB divergence and volatility-range mismatch."""
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    vol_ratio = features.get('volume_ratio', 1.0)
    vol_regime = features.get('volatility_regime', 0.5)
    range_pct = features.get('range_pct', 0.5)
    body_ratio = features.get('body_ratio', 0.5)
    
    # Skip: RSI extreme at Bollinger Band edge (reversal risk)
    if (rsi > 70 or rsi < 30) and (bb_pos > 0.95 or bb_pos < 0.05):
        return "skip"
    
    # Skip: high volatility but narrow range (breakout trap)
    if vol_regime > 0.7 and range_pct < 0.3:
        return "skip"
    
    # Skip: weak candle body without volume confirmation
    if body_ratio < 0.3 and vol_ratio < 0.8:
        return "skip"
    
    return prediction