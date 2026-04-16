def guard(features: dict, prediction: str) -> str:
    # Skip if price is too close to fair value (VWAP)
    if abs(features.get('vwap_deviation', 0)) < 0.002:
        return "skip"
    
    # Skip if RSI_2h is neutral (no directional conviction)
    if 45 <= features.get('rsi_2h', 50) <= 55:
        return "skip"
    
    return prediction