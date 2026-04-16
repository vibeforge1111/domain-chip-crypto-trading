def guard(features: dict, prediction: str) -> str:
    """Filter signals when both bb_pct_b and stoch_k show extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Extreme overbought: price at upper band + stoch confirms
    if prediction == 'long' and bb_pct_b > 0.92 and stoch_k > 85:
        return 'skip'
    
    # Extreme oversold: price at lower band + stoch confirms
    if prediction == 'short' and bb_pct_b < 0.08 and stoch_k < 15:
        return 'skip'
    
    return prediction