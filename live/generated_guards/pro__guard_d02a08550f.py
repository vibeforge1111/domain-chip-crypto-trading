def guard(features: dict, prediction: str) -> str:
    """Filter trades when Bollinger Band position contradicts the trade direction."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Price at lower band extremes - reject shorts
    if bb_pct_b < 0.05 and prediction == 'short':
        return 'skip'
    
    # Price at upper band extremes - reject longs
    if bb_pct_b > 0.95 and prediction == 'long':
        return 'skip'
    
    return prediction