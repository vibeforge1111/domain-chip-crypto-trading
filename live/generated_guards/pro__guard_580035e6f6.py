def guard(features: dict, prediction: str) -> str:
    """Reject trades at overbought/oversold extremes using BB position and Stochastic."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought extreme: BB at upper band AND Stochastic overbought
    if bb_pct > 0.9 and stoch_k > 80:
        return "skip"
    
    # Oversold extreme: BB at lower band AND Stochastic oversold
    if bb_pct < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction