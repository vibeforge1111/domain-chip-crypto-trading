def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using atr_ratio, bb_width, and momentum."""
    atr = features.get('atr_ratio', 1.0)
    bb_w = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    macd = features.get('macd_histogram', 0)
    
    # True compression: low volatility AND tight bands
    compressed = atr < 0.75 and bb_w < 0.35
    
    # Momentum absent: stochastic range-bound, MACD flat
    weak_momentum = abs(stoch_k - 50) < 15 and abs(stoch_d - 50) < 15 and abs(macd) < 0.0001
    
    # Reject compression setups without momentum confirmation
    if compressed and weak_momentum:
        return "skip"
    
    return prediction