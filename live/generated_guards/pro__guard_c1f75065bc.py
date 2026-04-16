def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using Bollinger Band position and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)

    # Reject longs when deeply overbought (both indicators confirm)
    if prediction == "long" and bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"

    # Reject shorts when deeply oversold (both indicators confirm)
    if prediction == "short" and bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"

    return prediction