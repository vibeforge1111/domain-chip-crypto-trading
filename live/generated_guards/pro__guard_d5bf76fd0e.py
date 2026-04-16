def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is stalling (histogram near zero)."""
    macd = features.get('macd_histogram', 0)
    # Skip if momentum is weak/consolidating (histogram near zero)
    if abs(macd) < 0.0002:
        return "skip"
    return prediction