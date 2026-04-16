def guard(features: dict, prediction: str) -> str:
    """Reject trades when wick-to-body ratio contradicts the predicted direction."""
    if prediction == "long":
        # Reject longs when upper wick dominates (selling pressure present)
        if features.get("upper_wick_ratio", 0) > 0.5 and features.get("body_ratio", 0) < 0.3:
            return "skip"
    elif prediction == "short":
        # Reject shorts when lower wick dominates (buying pressure present)
        if features.get("lower_wick_ratio", 0) > 0.5 and features.get("body_ratio", 0) < 0.3:
            return "skip"
    return prediction