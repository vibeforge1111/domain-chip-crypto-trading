def guard(features: dict, prediction: str) -> str:
    rsi_2h = features.get("rsi_2h", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Skip longs when broader trend (rsi_2h) is weak OR price at lower band extremes
    if prediction == "long" and (rsi_2h < 38 or bb_pct_b < 0.12):
        return "skip"
    # Skip shorts when broader trend (rsi_2h) is strong OR price at upper band extremes
    if prediction == "short" and (rsi_2h > 62 or bb_pct_b > 0.88):
        return "skip"
    return prediction