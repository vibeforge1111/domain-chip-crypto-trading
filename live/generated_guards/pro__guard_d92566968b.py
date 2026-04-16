def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating (weak macd_histogram with overbought/oversold)."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)

    # Skip longs when momentum decelerating into overbought
    if prediction == 'long' and 0 < macd_hist < 0.0003 and stoch_k > 75 and stoch_d > 75:
        return 'skip'

    # Skip shorts when momentum decelerating into oversold
    if prediction == 'short' and -0.0003 < macd_hist < 0 and stoch_k < 25 and stoch_d < 25:
        return 'skip'

    return prediction