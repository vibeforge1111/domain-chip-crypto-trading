def guard(features: dict, prediction: str) -> str:
    """Reject trades against Bollinger Band extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Reject longs when price is near upper band (overbought)
    if prediction == 'long' and bb_pct_b > 0.95:
        return 'skip'
    
    # Reject shorts when price is near lower band (oversold)
    if prediction == 'short' and bb_pct_b < 0.05:
        return 'skip'
    
    return prediction