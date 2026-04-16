def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only allow trades at extreme BB positions for high confidence entries
    if prediction == 'long':
        return prediction if bb_pct_b < 0.05 else 'skip'
    elif prediction == 'short':
        return prediction if bb_pct_b > 0.95 else 'skip'
    
    return prediction