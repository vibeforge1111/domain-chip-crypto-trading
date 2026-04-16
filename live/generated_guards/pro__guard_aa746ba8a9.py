def guard(features: dict, prediction: str) -> str:
    # Skip if price too far from VWAP (either direction signals exhaustion)
    if abs(features.get('vwap_deviation', 0)) > 0.015:
        return "skip"
    
    # Skip if momentum indicators disagree (RSI vs Stoch divergence)
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    rsi_14 = features.get('rsi_14', 50)
    
    if rsi_2h > 60 and stoch_k < 30:
        return "skip"
    if rsi_2h < 40 and stoch_k > 70:
        return "skip"
    if rsi_2h > 65 and rsi_14 < 40:
        return "skip"
    if rsi_2h < 35 and rsi_14 > 60:
        return "skip"
    
    return prediction