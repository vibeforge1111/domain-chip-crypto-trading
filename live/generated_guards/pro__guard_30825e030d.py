def guard(features: dict, prediction: str) -> str:
    """Filter trades based on momentum divergence and volatility confirmation."""
    # Skip if RSI extreme with conflicting momentum (divergence)
    if features['rsi_14'] > 70 and features['momentum_score'] < 0.25:
        return "skip"
    if features['rsi_14'] < 30 and features['momentum_score'] > 0.25:
        return "skip"
    
    # Skip if high volume spike but weak momentum (exhaustion)
    if features['volume_ratio'] > 1.8 and features['momentum_score'] < 0.3:
        return "skip"
    
    # Skip if high ATR with tight BBs (choppy, false moves)
    if features['atr_ratio'] > 1.6 and features['bb_width'] < 0.6:
        return "skip"
    
    return prediction