def guard(features: dict, prediction: str) -> str:
    """Filter trades with momentum-volume divergence."""
    momentum = features.get('momentum_score', 0)
    volume = features.get('volume_ratio', 1)
    
    # Strong momentum without volume confirmation suggests weak signal
    if abs(momentum) > 0.4 and volume < 0.6:
        return "skip"
    
    return prediction