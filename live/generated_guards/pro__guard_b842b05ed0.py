def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB position and Stochastic show extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when both BB upper band AND stoch > 80 (extreme overbought)
    if prediction == 'long' and bb_pct_b > 0.90 and stoch_k > 80:
        return 'skip'
    
    # Skip shorts when both BB lower band AND stoch < 20 (extreme oversold)
    if prediction == 'short' and bb_pct_b < 0.10 and stoch_k < 20:
        return 'skip'
    
    return prediction