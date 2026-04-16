def guard(features: dict, prediction: str) -> str:
    """Reject trades when price is at extreme overbought/oversold condition."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject long signals in extreme overbought (high BB position + high stochastic)
    if prediction == 'long' and bb_pct_b > 0.85 and stoch_k > 80:
        return 'skip'
    
    # Reject short signals in extreme oversold (low BB position + low stochastic)
    if prediction == 'short' and bb_pct_b < 0.15 and stoch_k < 20:
        return 'skip'
    
    return prediction