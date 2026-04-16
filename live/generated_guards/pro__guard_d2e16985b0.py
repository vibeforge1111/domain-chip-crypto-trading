def guard(features: dict, prediction: str) -> str:
    # Skip when stochastics and momentum are diverging (unstable setup)
    if prediction == "long":
        if features['stoch_k'] < 25 and features['momentum_score'] > 0.3:
            return "skip"
    elif prediction == "short":
        if features['stoch_k'] > 75 and features['momentum_score'] < -0.3:
            return "skip"
    
    # Skip when BB width is very tight but momentum is weak (low conviction)
    if features['bb_width'] < 0.015 and abs(features['momentum_score']) < 0.25:
        return "skip"
    
    return prediction