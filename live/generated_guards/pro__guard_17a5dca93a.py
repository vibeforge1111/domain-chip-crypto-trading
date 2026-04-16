def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones for high-confidence entries."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # High-confidence long entry: price at lower band extreme
    if bb_pct_b < 0.05 and prediction == 'short':
        return 'skip'
    
    # High-confidence short entry: price at upper band extreme
    if bb_pct_b > 0.95 and prediction == 'long':
        return 'skip'
    
    return prediction