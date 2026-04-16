def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with stochastic confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # High-confidence long: at lower band AND stochastic confirming
    if bb_pct_b < 0.05 and prediction == "long":
        return prediction
    # High-confidence short: at upper band AND stochastic confirming
    if bb_pct_b > 0.95 and prediction == "short":
        return prediction
    
    # Filter out contradictory trades at extremes
    if bb_pct_b < 0.05 and prediction == "short":
        return "skip"
    if bb_pct_b > 0.95 and prediction == "long":
        return "skip"
    
    # Require stochastic confirmation for non-extreme entries
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        if prediction == "long" and stoch_k < 30:
            return prediction
        if prediction == "short" and stoch_k > 70:
            return prediction
        return "skip"
    
    return prediction