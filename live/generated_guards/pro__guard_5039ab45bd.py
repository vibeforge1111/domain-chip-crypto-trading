def guard(features: dict, prediction: str) -> str:
    # Skip longs when overbought: bb_pct_b near upper band AND stoch_k elevated
    if prediction == "long" and features['bb_pct_b'] > 0.85 and features['stoch_k'] > 80:
        return "skip"
    # Skip shorts when oversold: bb_pct_b near lower band AND stoch_k depressed
    if prediction == "short" and features['bb_pct_b'] < 0.15 and features['stoch_k'] < 20:
        return "skip"
    return prediction