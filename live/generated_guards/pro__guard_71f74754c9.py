def guard(features: dict, prediction: str) -> str:
    """Reject trades in choppy/volatile conditions without confirmed trend."""
    # Skip if high volatility but weak trend (whipsaw-prone conditions)
    if features['atr_ratio'] > 1.5 and features['trend_strength'] < 0.4:
        return "skip"
    return prediction