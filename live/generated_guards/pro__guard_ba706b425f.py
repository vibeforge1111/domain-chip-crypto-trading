def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum diverges from trend or BB position lacks confirmation."""
    momentum = features.get('momentum_score', 0)
    trend = features.get('trend_strength', 0)
    bb_pos = features.get('bb_position', 0.5)
    ema_slope = features.get('ema_slope', 0)
    
    # Filter 1: Weak momentum in strong trend (likely exhaustion)
    if momentum < 0.2 and trend > 0.6:
        return "skip"
    
    # Filter 2: BB extreme without momentum confirmation
    if (bb_pos > 0.9 or bb_pos < 0.1) and abs(momentum) < 0.3:
        return "skip"
    
    # Filter 3: EMA direction contradicts prediction in strong trend
    if trend > 0.7 and ema_slope * (1 if prediction == "long" else -1) < 0:
        return "skip"
    
    return prediction