def guard(features: dict, prediction: str) -> str:
    """Filter trades on wick-dominated candles (reversal-prone structure)."""
    if prediction == "long" and features["upper_wick_ratio"] > features["body_ratio"]:
        return "skip"
    if prediction == "short" and features["lower_wick_ratio"] > features["body_ratio"]:
        return "skip"
    return prediction