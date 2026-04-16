def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB position and Stochastic show extreme overbought/oversold."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: price near upper BB and stochastic in extreme zone
    overbought = bb_pct_b > 0.88 and stoch_k > 80
    # Oversold: price near lower BB and stochastic in extreme zone
    oversold = bb_pct_b < 0.12 and stoch_k < 20
    
    if overbought or oversold:
        return "skip"
    
    return prediction