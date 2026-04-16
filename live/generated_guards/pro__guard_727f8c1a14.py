def guard(features: dict, prediction: str) -> str:
    # Reject longs when overbought (BB upper band + stochastic overbought + high 2h RSI)
    if prediction == "long" and features["bb_pct_b"] > 0.85 and features["stoch_k"] > 80 and features["rsi_2h"] > 70:
        return "skip"
    # Reject shorts when oversold (BB lower band + stochastic oversold + low 2h RSI)
    if prediction == "short" and features["bb_pct_b"] < 0.15 and features["stoch_k"] < 20 and features["rsi_2h"] < 30:
        return "skip"
    return prediction