def guard(features: dict, prediction: str) -> str:
    # Reject when both BB position and Stochastic confirm overbought
    if features['bb_pct_b'] > 0.92 and features['stoch_k'] > 82:
        return "skip"
    # Reject when both BB position and Stochastic confirm oversold
    if features['bb_pct_b'] < 0.08 and features['stoch_k'] < 18:
        return "skip"
    return prediction