def guard(features: dict, prediction: str) -> str:
    """Filter trades based on BB position and momentum alignment."""
    bb_position = features.get('bb_position', 0.5)
    momentum_score = features.get('momentum_score', 0)
    
    if prediction == 'long':
        if bb_position > 0.85 or momentum_score < 0.15:
            return 'skip'
    elif prediction == 'short':
        if bb_position < 0.15 or momentum_score > -0.15:
            return 'skip'
    
    return prediction