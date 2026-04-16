def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value using VWAP deviation with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Skip if price is very close to VWAP (< 0.15%) AND stochastics are extreme
    if abs(vwap_dev) < 0.0015 and (stoch_k > 80 or stoch_k < 20 or stoch_d > 80 or stoch_d < 20):
        return "skip"
    
    # Skip if price too close to VWAP in extreme 2h RSI regime
    if abs(vwap_dev) < 0.001 and (rsi_2h > 72 or rsi_2h < 28):
        return "skip"
    
    return prediction