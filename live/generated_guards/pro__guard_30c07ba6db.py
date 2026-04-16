def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme Bollinger Band positions as entry zones."""
    bb_extreme_long = features["bb_pct_b"] < 0.05
    bb_extreme_short = features["bb_pct_b"] > 0.95
    if prediction == "long" and not bb_extreme_long:
        return "skip"
    if prediction == "short" and not bb_extreme_short:
        return "skip"
    return prediction