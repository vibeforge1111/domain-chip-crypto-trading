def guard(features: dict, prediction: str) -> str:
    """Filter out momentum divergence with extreme band position."""
    if (features['rsi_14'] > 70 and features['bb_position'] > 0.9) or (features['rsi_14'] < 30 and features['bb_position'] < 0.1):
        return "skip"
    return prediction