def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB and Stochastic show extreme overbought/oversold."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Reject longs when both indicators are at overbought extremes
    if prediction == 'long' and bb_pct > 0.92 and stoch > 80:
        return 'skip'
    
    # Reject shorts when both indicators are at oversold extremes
    if prediction == 'short' and bb_pct < 0.08 and stoch < 20:
        return 'skip'
    
    return prediction