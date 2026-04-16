def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when overbought: price near upper band + stoch > 80
    if prediction == "long" and bb_pct_b > 0.85 and stoch_k > 80:
        return "skip"
    
    # Skip shorts when oversold: price near lower band + stoch < 20
    if prediction == "short" and bb_pct_b < 0.15 and stoch_k < 20:
        return "skip"
    
    return prediction