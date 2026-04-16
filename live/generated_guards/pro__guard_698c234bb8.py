def guard(features: dict, prediction: str) -> str:
    # Skip in compression when stochastic is extreme (likely reversal, not breakout)
    if features['atr_ratio'] < 0.75 and features['bb_width'] < 0.2:
        if features['stoch_k'] > 80 or features['stoch_k'] < 20:
            return "skip"
    return prediction