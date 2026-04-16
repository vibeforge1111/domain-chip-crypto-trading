def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using rsi_2h."""
    rsi_2h = features.get('rsi_2h', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Long: require favorable 2h context and price above VWAP
    if prediction == "long" and (rsi_2h < 45 or vwap_dev < -0.005):
        return "skip"
    # Short: require unfavorable 2h context and price below VWAP
    if prediction == "short" and (rsi_2h > 55 or vwap_dev > 0.005):
        return "skip"
    return prediction