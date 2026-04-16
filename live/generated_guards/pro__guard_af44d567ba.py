def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum lacks conviction (macd_histogram near zero)."""
    macd = features.get('macd_histogram', 0)
    if abs(macd) < 0.0001:  # Momentum signal too weak
        return "skip"
    return prediction