def guard(features: dict, prediction: str) -> str:
    """Filter trades where VWAP deviation disagrees with momentum indicators."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    macd = features.get('macd_histogram', 0)
    obv = features.get('obv_slope', 0)
    
    # Price extended above VWAP but momentum fading
    if vwap_dev > 0.006 and momentum < -0.05 and macd < 0:
        return "skip"
    
    # Price extended below VWAP but momentum building
    if vwap_dev < -0.006 and momentum > 0.05 and macd > 0:
        return "skip"
    
    # VWAP divergence with volume/OBV confirmation
    if abs(vwap_dev) > 0.008 and obv * vwap_dev < 0:
        return "skip"
    
    return prediction