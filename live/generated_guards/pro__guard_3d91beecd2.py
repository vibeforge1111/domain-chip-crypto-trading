def guard(features: dict, prediction: str) -> str:
    """Reject trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    if prediction == "long" and bb_pct > 0.85 and stoch > 80:
        return "skip"
    if prediction == "short" and bb_pct < 0.15 and stoch < 20:
        return "skip"
    return prediction