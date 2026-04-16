def guard(features: dict, prediction: str) -> str:
    # Skip if both bb_pct_b and stoch_k indicate overbought extremes
    if features['bb_pct_b'] > 0.92 and features['stoch_k'] > 80:
        return "skip"
    # Skip if both bb_pct_b and stoch_k indicate oversold extremes
    if features['bb_pct_b'] < 0.08 and features['stoch_k'] < 20:
        return "skip"
    return prediction