def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum diverges from the predicted direction."""
    macd = features.get("macd_histogram", 0)
    
    # Long prediction requires bullish momentum (positive histogram)
    if prediction == "long" and macd < -0.0003:
        return "skip"
    
    # Short prediction requires bearish momentum (negative histogram)
    if prediction == "short" and macd > 0.0003:
        return "skip"
    
    return prediction