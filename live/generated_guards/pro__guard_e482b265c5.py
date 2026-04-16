def guard(features: dict, prediction: str) -> str:
    """Guard using Bollinger Band extremes and stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == "long":
        # Accept longs only near lower band or with oversold stoch
        if bb_pct_b > 0.12 and stoch_k > 35:
            return "skip"
    
    if prediction == "short":
        # Accept shorts only near upper band or with overbought stoch
        if bb_pct_b < 0.88 and stoch_k < 65:
            return "skip"
    
    return prediction