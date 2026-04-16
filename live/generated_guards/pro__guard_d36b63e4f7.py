def guard(features: dict, prediction: str) -> str:
    # Skip if too close to fair value (VWAP deviation near zero)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    # Skip longs if overbought on higher timeframe
    if prediction == "long" and features.get('rsi_2h', 50) > 72:
        return "skip"
    # Skip shorts if oversold on higher timeframe
    if prediction == "short" and features.get('rsi_2h', 50) < 28:
        return "skip"
    return prediction