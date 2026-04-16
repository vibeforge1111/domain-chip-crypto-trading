def guard(features: dict, prediction: str) -> str:
    """Filter trades with weak momentum alignment and poor candle structure."""
    if prediction == "long":
        # Reject if upper wick dominates (rejection from above) and momentum not supportive
        if features["upper_wick_ratio"] > 0.5 and features["momentum_score"] < 0:
            return "skip"
    elif prediction == "short":
        # Reject if lower wick dominates (rejection from below) and momentum not supportive
        if features["lower_wick_ratio"] > 0.5 and features["momentum_score"] > 0:
            return "skip"
    return prediction