def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions with stochastic confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    if prediction == "long":
        if not (bb < 0.05 and stoch < 20):
            return "skip"
    elif prediction == "short":
        if not (bb > 0.95 and stoch > 80):
            return "skip"
    
    return prediction