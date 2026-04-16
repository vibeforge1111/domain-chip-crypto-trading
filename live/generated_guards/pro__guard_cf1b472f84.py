def guard(features: dict, prediction: str) -> str:
    bb = features.get('bb_pct_b', 0.5)
    vwap = features.get('vwap_deviation', 0)
    stoch = features.get('stoch_k', 50)
    # High-confidence entries only at BB extremes with confirmation
    if bb < 0.05 and vwap < 0 and stoch < 30:
        return prediction
    if bb > 0.95 and vwap > 0 and stoch > 70:
        return prediction
    return "skip"