def guard(features: dict, prediction: str) -> str:
    """Skip trades when Bollinger position and Stochastic show extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Long signals at extreme overbought: skip
    if prediction == 'long' and bb_pct_b > 0.88 and stoch_k > 80:
        return 'skip'
    
    # Short signals at extreme oversold: skip
    if prediction == 'short' and bb_pct_b < 0.12 and stoch_k < 20:
        return 'skip'
    
    return prediction