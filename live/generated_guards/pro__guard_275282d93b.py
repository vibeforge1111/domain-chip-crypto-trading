def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones as high-confidence entry points."""
    if prediction == "skip":
        return prediction
    bb = features.get("bb_pct_b", 0.5)
    if prediction == "long" and bb >= 0.05:
        return "skip"
    if prediction == "short" and bb <= 0.95:
        return "skip"
    return prediction