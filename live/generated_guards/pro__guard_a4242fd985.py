def guard(features: dict, prediction: str) -> str:
    """Filter trades at extreme overbought/oversold levels using BB position and Stochastic."""
    # Skip longs when price at top of BB AND stochastic overbought
    if prediction == "long" and features['bb_pct_b'] > 0.85 and features['stoch_k'] > 80:
        return "skip"
    # Skip shorts when price at bottom of BB AND stochastic oversold
    if prediction == "short" and features['bb_pct_b'] < 0.15 and features['stoch_k'] < 20:
        return "skip"
    return prediction