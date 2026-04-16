def guard(features: dict, prediction: str) -> str:
    """Skip trades when both BB and Stochastic confirm extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if both indicators confirm overbought (reversal risk)
    if bb_pct_b > 0.9 and stoch_k > 80:
        return "skip"
    
    # Skip if both indicators confirm oversold (potential reversal trap)
    if bb_pct_b < 0.1 and stoch_k < 20:
        return "skip"
    
    return prediction