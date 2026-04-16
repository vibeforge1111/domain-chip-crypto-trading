def guard(features: dict, prediction: str) -> str:
    """Reject trades when both Bollinger Bands position and Stochastic confirm extreme overbought/oversold."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Overbought: price at upper band AND stoch > 80
    overbought = bb_pct_b > 0.85 and stoch_k > 80
    
    # Oversold: price at lower band AND stoch < 20
    oversold = bb_pct_b < 0.15 and stoch_k < 20
    
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction