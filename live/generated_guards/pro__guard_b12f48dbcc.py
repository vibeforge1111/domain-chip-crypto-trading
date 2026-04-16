def guard(features: dict, prediction: str) -> str:
    """Skip trades when both stochastic and Bollinger position confirm extremes."""
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if prediction == "long":
        # Reject longs when overbought: both oscillators confirm
        if stoch_k > 80 and bb_pct_b > 0.85:
            return "skip"
    elif prediction == "short":
        # Reject shorts when oversold: both oscillators confirm
        if stoch_k < 20 and bb_pct_b < 0.15:
            return "skip"
    return prediction