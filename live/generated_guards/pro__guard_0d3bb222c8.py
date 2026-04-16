def guard(features: dict, prediction: str) -> str:
    """Skip trades when both Bollinger position and Stochastic confirm extremes."""
    if prediction == "long" and features['bb_pct_b'] > 0.88 and features['stoch_k'] > 85:
        return "skip"
    if prediction == "short" and features['bb_pct_b'] < 0.12 and features['stoch_k'] < 15:
        return "skip"
    return prediction