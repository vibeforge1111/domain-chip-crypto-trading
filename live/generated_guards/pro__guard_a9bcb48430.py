def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Only allow trades at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # At lower BB extreme, confirm with stoch (oversold)
    if bb_pct_b < 0.05 and stoch_k > 40:
        return "skip"
    
    # At upper BB extreme, confirm with stoch (overbought)
    if bb_pct_b > 0.95 and stoch_k < 60:
        return "skip"
    
    return prediction