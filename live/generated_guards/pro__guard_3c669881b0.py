def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    
    # Only allow entries at extreme BB positions (<0.05 or >0.95) with RSI confirmation
    if prediction == 'long' and bb_pct_b < 0.05 and rsi_14 < 35:
        return prediction
    if prediction == 'short' and bb_pct_b > 0.95 and rsi_14 > 65:
        return prediction
    
    return 'skip'