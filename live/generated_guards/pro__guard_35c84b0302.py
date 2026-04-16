def guard(features: dict, prediction: str) -> str:
    """Filter trades to only allow entries in extreme bb_pct_b zones."""
    bb = features.get('bb_pct_b', 0.5)
    # Long only near lower band, short only near upper band
    if prediction == "long" and bb >= 0.05:
        return "skip"
    if prediction == "short" and bb <= 0.95:
        return "skip"
    return prediction