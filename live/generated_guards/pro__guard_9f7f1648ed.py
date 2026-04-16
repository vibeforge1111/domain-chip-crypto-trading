def guard(features: dict, prediction: str) -> str:
    """Skip when both Bollinger Bands and Stochastic are in extreme territory."""
    if features['bb_pct_b'] > 0.9 and features['stoch_k'] > 80:
        return "skip"
    if features['bb_pct_b'] < 0.1 and features['stoch_k'] < 20:
        return "skip"
    return prediction