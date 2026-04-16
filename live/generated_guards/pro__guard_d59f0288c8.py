def guard(features: dict, prediction: str) -> str:
    """Guard function filtering trades based on stochastic crossover quality."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)

    if prediction == 'long':
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_k - stoch_d < 5:
            return "skip"
        if stoch_k > 80 or stoch_k < 20:
            return "skip"
        if bb_pct_b > 0.9 or vwap_dev < 0:
            return "skip"
        if rsi_2h < 45:
            return "skip"

    elif prediction == 'short':
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_d - stoch_k < 5:
            return "skip"
        if stoch_k < 20 or stoch_k > 80:
            return "skip"
        if bb_pct_b < 0.1 or vwap_dev > 0:
            return "skip"
        if rsi_2h > 55:
            return "skip"

    return prediction