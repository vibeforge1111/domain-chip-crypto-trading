def guard(features: dict, prediction: str) -> str:
    """Reject trades at confirmed overbought/oversold extremes using Bollinger and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)

    # Reject longs when both BB at upper band AND Stochastic overbought
    if prediction == "long" and bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"

    # Reject shorts when both BB at lower band AND Stochastic oversold
    if prediction == "short" and bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"

    return prediction