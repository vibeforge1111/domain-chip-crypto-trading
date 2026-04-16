def guard(features: dict, prediction: str) -> str:
    """Filter trades with extreme VWAP deviation + overbought/oversold RSI."""
    vwap_dev = abs(features.get("vwap_deviation", 0))
    rsi = features.get("rsi_14", 50)
    vol_regime = features.get("volatility_regime", 0.5)
    
    # Reject if price far from VWAP (>1%) AND RSI extreme
    if vwap_dev > 0.01 and (rsi > 70 or rsi < 30):
        return "skip"
    
    # Also reject in high volatility with conflicting signals
    if vol_regime > 0.7 and vwap_dev > 0.005 and rsi > 65:
        return "skip"
    
    return prediction