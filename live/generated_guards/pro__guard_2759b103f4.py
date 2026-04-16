def guard(features: dict, prediction: str) -> str:
    """Filter signals when momentum contradicts RSI extremes or volatility spikes occur."""
    rsi = features.get("rsi_14", 50)
    momentum = features.get("momentum_score", 0)
    volatility = features.get("volatility_regime", 0)
    range_pct = features.get("range_pct", 0)
    
    # Momentum divergence during RSI extremes (exhaustion signal)
    rsi_extreme = rsi > 70 or rsi < 30
    momentum_weak = abs(momentum) < 0.2
    if rsi_extreme and momentum_weak:
        return "skip"
    
    # High volatility spike with large candles (reversal risk)
    if volatility > 1.5 and range_pct > 2.0:
        return "skip"
    
    return prediction