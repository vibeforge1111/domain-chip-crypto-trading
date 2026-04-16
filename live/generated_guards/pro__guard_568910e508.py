def guard(features: dict, prediction: str) -> str:
    """Filter trades based on RSI-Momentum divergence and volume confirmation."""
    # Skip if volume is too low (insufficient market participation)
    if features['volume_ratio'] < 0.5:
        return "skip"
    
    # Detect divergence: when RSI and momentum strongly disagree
    rsi_centered = abs(features['rsi_14'] - 50)
    momentum_centered = abs(features['momentum_score'] * 100 - 50)
    
    # Skip if significant divergence (>25 points apart from center)
    if abs(rsi_centered - momentum_centered) > 25:
        return "skip"
    
    # Skip if at extreme BB position with weak momentum
    if features['bb_pct_b'] > 0.88 and features['momentum_score'] < 0.3:
        return "skip"
    
    return prediction