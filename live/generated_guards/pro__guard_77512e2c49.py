def guard(features: dict, prediction: str) -> str:
    """Reject trades with extreme RSI lacking trend confirmation."""
    if (features['rsi_14'] > 72 or features['rsi_14'] < 28) and features['trend_strength'] < 0.4:
        return "skip"
    return prediction