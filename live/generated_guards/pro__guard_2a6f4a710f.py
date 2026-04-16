def guard(features: dict, prediction: str) -> str:
    """Reject longs at overbought extremes, shorts at oversold extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)

    # Overbought: BB upper band + stochastic extreme + RSI confirmation
    if prediction == 'long' and bb_pct_b > 0.90 and stoch_k > 80 and stoch_d > 80:
        if rsi_2h > 65:
            return 'skip'

    # Oversold: BB lower band + stochastic extreme + RSI confirmation
    if prediction == 'short' and bb_pct_b < 0.10 and stoch_k < 20 and stoch_d < 20:
        if rsi_2h < 35:
            return 'skip'

    return prediction