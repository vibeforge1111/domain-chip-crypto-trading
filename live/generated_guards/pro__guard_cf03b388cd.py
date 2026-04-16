def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (negative MACD histogram)."""
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    
    # Skip if momentum decelerating AND overbought
    if macd < 0 and stoch > 80:
        return "skip"
    return prediction