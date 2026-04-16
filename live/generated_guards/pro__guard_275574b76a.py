def guard(features: dict, prediction: str) -> str:
    """Skip trades at extreme BB position during low volatility (choppy consolidation)."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    volatility_regime = features.get('volatility_regime', 0.5)
    
    # Reject when price is at BB extremes during low volatility (false breakout risk)
    if (bb_pct_b < 0.1 or bb_pct_b > 0.9) and volatility_regime < 0.35:
        return "skip"
    
    return prediction