def guard(features: dict, prediction: str) -> str:
    # Skip long if RSI overbought and momentum weak
    if prediction == "long" and features['rsi_14'] > 70 and features['momentum_score'] < 0.4:
        return "skip"
    
    # Skip short if RSI oversold and momentum weak
    if prediction == "short" and features['rsi_14'] < 30 and features['momentum_score'] > -0.4:
        return "skip"
    
    return prediction