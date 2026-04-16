def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones."""
    bb = features.get('bb_pct_b', 0.5)
    
    # Long only when near lower band, short only when near upper band
    if prediction == 'long' and bb > 0.10:
        return 'skip'
    if prediction == 'short' and bb < 0.90:
        return 'skip'
    
    return prediction