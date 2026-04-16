def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB and Stochastic confirm extreme overbought/oversold."""
    # Long signals: reject when overbought (bb at upper band + stochastic above 80)
    if prediction == "long" and features.get("bb_pct_b", 0) > 0.85 and features.get("stoch_k", 0) > 80:
        return "skip"
    # Short signals: reject when oversold (bb at lower band + stochastic below 20)
    if prediction == "short" and features.get("bb_pct_b", 0) < 0.15 and features.get("stoch_k", 0) < 20:
        return "skip"
    return prediction