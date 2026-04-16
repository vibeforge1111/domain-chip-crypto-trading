def guard(features: dict, prediction: str) -> str:
    # Filter trades too close to fair value (low edge near VWAP)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Avoid overbought/oversold stochastic extremes
    if features.get('stoch_k', 50) > 80 or features.get('stoch_k', 50) < 20:
        return "skip"
    return prediction