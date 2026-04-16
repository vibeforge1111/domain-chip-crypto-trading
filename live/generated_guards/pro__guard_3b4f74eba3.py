def guard(features: dict, prediction: str) -> str:
    """Rejects trades where momentum contradicts trend direction."""
    if prediction == "long":
        if features['rsi_14'] < 50 and features['momentum_score'] < 0:
            return "skip"
    elif prediction == "short":
        if features['rsi_14'] > 50 and features['momentum_score'] > 0:
            return "skip"
    return prediction