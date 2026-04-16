def guard(features: dict, prediction: str) -> str:
    """Guard against trading at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    if prediction == 'long':
        if bb_pct > 0.85 and stoch > 80:
            return "skip"
    elif prediction == 'short':
        if bb_pct < 0.15 and stoch < 20:
            return "skip"
    
    return prediction