def guard(features: dict, prediction: str) -> str:
    """Detect overbought/oversold extremes using BB position and Stochastic."""
    # Skip if both BB position and Stochastic indicate extreme overbought
    if features['bb_pct_b'] > 0.85 and features['stoch_k'] > 80:
        return "skip"
    # Skip if both indicators show extreme oversold
    if features['bb_pct_b'] < 0.15 and features['stoch_k'] < 20:
        return "skip"
    return prediction