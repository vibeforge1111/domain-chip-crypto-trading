def guard(features: dict, prediction: str) -> str:
    """Skip trades when both BB position and Stochastic confirm extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought: both BB at upper band and stochastic extreme
    if prediction == 'long' and bb_pct_b > 0.9 and stoch_k > 80:
        return 'skip'
    
    # Oversold: both BB at lower band and stochastic extreme
    if prediction == 'short' and bb_pct_b < 0.1 and stoch_k < 20:
        return 'skip'
    
    return prediction