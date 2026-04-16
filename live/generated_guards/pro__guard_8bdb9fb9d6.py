def guard(features: dict, prediction: str) -> str:
    """Skip trades where VWAP deviation and momentum score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)

    if prediction == 'long':
        if vwap_dev > 0.004 and momentum < -0.1:
            return 'skip'
        if rsi_2h > 70 and momentum < 0:
            return 'skip'

    if prediction == 'short':
        if vwap_dev < -0.004 and momentum > 0.1:
            return 'skip'
        if rsi_2h < 30 and momentum > 0:
            return 'skip'

    return prediction