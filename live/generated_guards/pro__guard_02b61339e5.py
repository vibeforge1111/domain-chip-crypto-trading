def guard(features: dict, prediction: str) -> str:
    # Reject signals with strong momentum but low volatility (weak conviction)
    if features['momentum_score'] > 0.6 and features['volatility_regime'] < 0.4:
        return "skip"
    return prediction