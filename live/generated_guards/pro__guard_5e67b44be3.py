def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Reject long signals when both indicators confirm overbought
    if prediction == 'long' and bb_pct > 0.90 and stoch > 80:
        return 'skip'
    
    # Reject short signals when both indicators confirm oversold
    if prediction == 'short' and bb_pct < 0.10 and stoch < 20:
        return 'skip'
    
    return prediction