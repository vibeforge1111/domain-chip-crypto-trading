def guard(features: dict, prediction: str) -> str:
    """Reject trades with divergent candle body strength and momentum indicators."""
    body_ratio = features.get('body_ratio', 0.5)
    momentum_score = features.get('momentum_score', 0.5)
    bb_position = features.get('bb_position', 0.5)
    
    # Body-momentum alignment check
    if prediction == 'long':
        # Strong body but momentum near zero = false strength
        if body_ratio > 0.65 and momentum_score < 0.25:
            return "skip"
        # Body near extremes of Bollinger Band with weak body
        if bb_position > 0.9 and body_ratio < 0.35:
            return "skip"
    
    elif prediction == 'short':
        # Strong bearish body but momentum still positive = reversal risk
        if body_ratio > 0.65 and momentum_score > 0.75:
            return "skip"
        if bb_position < 0.1 and body_ratio < 0.35:
            return "skip"
    
    return prediction