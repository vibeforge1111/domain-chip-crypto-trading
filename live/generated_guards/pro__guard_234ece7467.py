def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB position and Stochastic confirm overbought/oversold extremes."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip longs when overbought (high BB position + high stochastic)
    if prediction == 'long' and bb_pct > 0.9 and stoch > 80:
        return 'skip'
    
    # Skip shorts when oversold (low BB position + low stochastic)
    if prediction == 'short' and bb_pct < 0.1 and stoch < 20:
        return 'skip'
    
    return prediction