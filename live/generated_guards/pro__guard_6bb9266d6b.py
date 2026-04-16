def guard(features: dict, prediction: str) -> str:
    # Skip if momentum decelerating (neg macd_histogram) while price at upper bands (divergence risk)
    if features['macd_histogram'] < -0.0003 and features['bb_pct_b'] > 0.85:
        return "skip"
    return prediction