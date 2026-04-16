def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes."""
    bb = features.get('bb_pct_b', 0.5)
    
    # Only trade at BB extremes: <0.05 (lower band) or >0.95 (upper band)
    if bb < 0.05 or bb > 0.95:
        return prediction
    
    return "skip"