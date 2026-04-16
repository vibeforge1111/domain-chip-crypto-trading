def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject overbought long signals
    if prediction == 'long' and bb_pct_b > 0.90 and stoch_k > 80:
        return 'skip'
    
    # Reject oversold short signals
    if prediction == 'short' and bb_pct_b < 0.10 and stoch_k < 20:
        return 'skip'
    
    return prediction