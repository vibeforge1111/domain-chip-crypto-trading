def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak momentum confirmation or unstable volatility."""
    momentum = features.get('momentum_score', 0)
    volume_ratio = features.get('volume_ratio', 1)
    atr_ratio = features.get('atr_ratio', 1)
    range_pct = features.get('range_pct', 0)
    
    # Skip if strong momentum but weak volume (no conviction)
    if momentum > 0.6 and volume_ratio < 0.6:
        return "skip"
    
    # Skip if high ATR but narrow range (choppy/volatile but no progress)
    if atr_ratio > 1.4 and range_pct < 0.5:
        return "skip"
    
    return prediction