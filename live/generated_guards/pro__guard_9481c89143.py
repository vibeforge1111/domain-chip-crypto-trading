def guard(features: dict, prediction: str) -> str:
    """Reject trades when both Bollinger Bands and Stochastic show extreme readings."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)

    # Skip longs when overbought on both BB and Stochastic
    if prediction == 'long' and bb_pct_b > 0.9 and stoch_k > 80:
        return 'skip'

    # Skip shorts when oversold on both BB and Stochastic
    if prediction == 'short' and bb_pct_b < 0.1 and stoch_k < 20:
        return 'skip'

    # Skip if 2h RSI contradicts the trade direction
    if prediction == 'long' and rsi_2h > 70:
        return 'skip'
    if prediction == 'short' and rsi_2h < 30:
        return 'skip'

    return prediction