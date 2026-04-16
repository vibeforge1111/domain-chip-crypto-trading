def guard(features: dict, prediction: str) -> str:
    """Filter trades based on momentum-RSI divergence and weak volume squeeze."""
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    bb_pos = features.get('bb_position', 0.5)
    volume_ratio = features.get('volume_ratio', 1)
    
    # Skip if RSI extreme but momentum contradicts direction (divergence)
    if rsi > 70 and momentum < -0.1:
        return "skip"
    if rsi < 30 and momentum > 0.1:
        return "skip"
    
    # Skip if extreme BB position with suspiciously low volume (weak squeeze)
    if (bb_pos > 0.92 or bb_pos < 0.08) and volume_ratio < 0.75:
        return "skip"
    
    return prediction