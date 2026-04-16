def guard(features: dict, prediction: str) -> str:
    """Skip on VWAP-momentum disagreement or RSI divergence."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_14 = features.get('rsi_14', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # VWAP and momentum disagreement: skip if conflicting signals
    if (vwap_dev > 0.005 and momentum < -0.15) or (vwap_dev < -0.005 and momentum > 0.15):
        return "skip"
    
    # Short vs longer RSI divergence: skip on strong disagreement
    if abs(rsi_14 - rsi_2h) > 25:
        return "skip"
    
    return prediction