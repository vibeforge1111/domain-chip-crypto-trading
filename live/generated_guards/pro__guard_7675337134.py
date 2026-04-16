def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)

    if prediction == 'long':
        if not (stoch_k > stoch_d and stoch_k < 35 and rsi_2h < 70 and vwap_dev > -0.01):
            return "skip"
    elif prediction == 'short':
        if not (stoch_k < stoch_d and stoch_k > 65 and rsi_2h > 30 and vwap_dev < 0.01):
            return "skip"

    return prediction