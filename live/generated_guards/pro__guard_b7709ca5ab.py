def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb = features.get('bb_pct_b', 0.5)
    sk = features.get('stoch_k', 50)
    
    if prediction == "long" and bb > 0.85 and sk > 80:
        return "skip"
    if prediction == "short" and bb < 0.15 and sk < 20:
        return "skip"
    
    return prediction