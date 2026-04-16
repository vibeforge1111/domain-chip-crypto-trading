def guard(features: dict, prediction: str) -> str:
    """Skip trades at confirmed overbought/oversold extremes using BB and Stoch."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Overbought: BB at upper band AND Stochastic confirms
    if prediction == 'long' and bb_pct_b > 0.88 and stoch_k > 85:
        return "skip"
    
    # Oversold: BB at lower band AND Stochastic confirms
    if prediction == 'short' and bb_pct_b < 0.12 and stoch_k < 15:
        return "skip"
    
    return prediction