def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB position and Stochastic show extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    if prediction == 'long' and bb_pct_b > 0.88 and stoch_k > 78:
        return 'skip'
    if prediction == 'short' and bb_pct_b < 0.12 and stoch_k < 22:
        return 'skip'
    
    return prediction