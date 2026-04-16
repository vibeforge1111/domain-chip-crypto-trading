def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating against the prediction direction."""
    macd = features.get('macd_histogram', 0)
    if prediction == 'long' and macd < 0:
        return 'skip'
    if prediction == 'short' and macd > 0:
        return 'skip'
    return prediction