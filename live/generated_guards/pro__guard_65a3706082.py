def guard(features: dict, prediction: str) -> str:
    """Skip trades when both BB position and Stochastic signal extreme overbought/oversold."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Overbought: price at upper BB and stochastic in overbought zone
    overbought = bb_pct > 0.90 and stoch_k > 85
    # Oversold: price at lower BB and stochastic in oversold zone
    oversold = bb_pct < 0.10 and stoch_k < 15
    
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    return prediction