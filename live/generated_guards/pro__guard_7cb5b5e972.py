def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    bb_pct_b = features.get("bb_pct_b", 0.5)
    if (prediction == "long" and bb_pct_b >= 0.05) or (prediction == "short" and bb_pct_b <= 0.95):
        return "skip"
    return prediction