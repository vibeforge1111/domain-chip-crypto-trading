def guard(features: dict, prediction: str) -> str:
    """Filter trades with disagreement between VWAP deviation and momentum."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Disagreement: price far below VWAP but bullish momentum with confirm from higher timeframe
    if vwap_dev < -0.015 and momentum > 0.25 and rsi_2h > 55:
        return "skip"
    
    # Disagreement: price far above VWAP but bearish momentum with confirm from higher timeframe
    if vwap_dev > 0.015 and momentum < -0.25 and rsi_2h < 45:
        return "skip"
    
    return prediction