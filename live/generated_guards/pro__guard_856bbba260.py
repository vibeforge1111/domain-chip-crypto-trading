def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones and stochastic confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    if prediction == "long":
        # Require lower band extreme and stochastic oversold confirmation
        if bb_pct_b > 0.10 or stoch_k > 30:
            return "skip"
    elif prediction == "short":
        # Require upper band extreme and stochastic overbought confirmation
        if bb_pct_b < 0.90 or stoch_k < 70:
            return "skip"
    
    return prediction