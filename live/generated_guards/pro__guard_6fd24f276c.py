def guard(features: dict, prediction: str) -> str:
    """Filter trades when both BB position and Stochastic show extreme conditions."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    # Skip longs when overbought: bb near upper band AND stoch > 80
    if prediction == 'long' and bb > 0.85 and stoch > 80:
        return 'skip'
    
    # Skip shorts when oversold: bb near lower band AND stoch < 20
    if prediction == 'short' and bb < 0.15 and stoch < 20:
        return 'skip'
    
    return prediction