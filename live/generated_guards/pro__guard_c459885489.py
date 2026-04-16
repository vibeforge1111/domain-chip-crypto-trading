def guard(features: dict, prediction: str) -> str:
    """Reject entries when not at BB extremes (high-confidence zones)."""
    bb_pct = features.get('bb_pct_b', 0.5)
    volume = features.get('volume_ratio', 1.0)
    
    if prediction == 'long':
        # Long only at lower BB extreme with confirming volume
        if bb_pct > 0.20 or volume < 0.8:
            return 'skip'
    elif prediction == 'short':
        # Short only at upper BB extreme with confirming volume
        if bb_pct < 0.80 or volume < 0.8:
            return 'skip'
    
    return prediction