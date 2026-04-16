def guard(features: dict, prediction: str) -> str:
    """Filter: Skip momentum trades without volume confirmation at extremes."""
    # In overbought/oversold zones, require volume for momentum signals
    if prediction == "long" and features['rsi_14'] > 65:
        if features['volume_ratio'] < 1.3:
            return "skip"
    if prediction == "short" and features['rsi_14'] < 35:
        if features['volume_ratio'] < 1.3:
            return "skip"
    return prediction