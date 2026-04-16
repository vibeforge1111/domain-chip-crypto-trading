def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to VWAP (fair value) using vwap_deviation."""
    # Skip if price is within 0.3% of VWAP (no clear directional bias)
    if abs(features.get('vwap_deviation', 0)) < 0.003:
        return "skip"
    
    # Skip longs when overbought on stochastic
    if prediction == "long" and features.get('stoch_k', 50) > 80:
        return "skip"
    
    # Skip shorts when oversold on stochastic
    if prediction == "short" and features.get('stoch_k', 50) < 20:
        return "skip"
    
    return prediction