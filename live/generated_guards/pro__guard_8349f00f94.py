def guard(features: dict, prediction: str) -> str:
    """Reject signals at Bollinger Band extremes with weak momentum and low volatility."""
    bb_pos = features.get('bb_position', 0.5)
    momentum = features.get('momentum_score', 0.5)
    volatility = features.get('volatility_regime', 0.5)
    
    # Skip when price is at band extremes but lacks momentum and volatility confirmation
    if (bb_pos > 0.92 or bb_pos < 0.08) and momentum < 0.35 and volatility < 0.4:
        return "skip"
    return prediction