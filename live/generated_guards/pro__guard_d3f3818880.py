def guard(features: dict, prediction: str) -> str:
    """Reject trades with momentum-trend divergence and extreme RSI."""
    if prediction == "skip":
        return prediction
    
    # Skip if momentum contradicts trend direction
    momentum_aligned_long = features["momentum_score"] > 0.3 and features["ema_slope"] > 0
    momentum_aligned_short = features["momentum_score"] < -0.3 and features["ema_slope"] < 0
    
    if prediction == "long" and not momentum_aligned_long:
        return "skip"
    if prediction == "short" and not momentum_aligned_short:
        return "skip"
    
    # Additional RSI extreme filter
    if prediction == "long" and features["rsi_14"] > 72:
        return "skip"
    if prediction == "short" and features["rsi_14"] < 28:
        return "skip"
    
    return prediction