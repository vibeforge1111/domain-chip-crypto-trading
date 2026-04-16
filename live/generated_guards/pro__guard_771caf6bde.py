def guard(features: dict, prediction: str) -> str:
    # Filter trades too close to fair value (VWAP) - no directional edge
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    # Skip if overbought/oversold without momentum alignment
    stoch_k = features.get('stoch_k', 50)
    momentum = features.get('momentum_score', 0)
    if stoch_k > 80 and momentum < 0:
        return "skip"
    if stoch_k < 20 and momentum > 0:
        return "skip"
    return prediction