def guard(features: dict, prediction: str) -> str:
    sk = features.get("stoch_k", 50)
    sd = features.get("stoch_d", 50)
    
    # For long: require stoch_k above stoch_d with D in oversold zone
    if prediction == "long" and not (sk > sd and sd < 30):
        return "skip"
    # For short: require stoch_k below stoch_d with K in overbought zone
    if prediction == "short" and not (sk < sd and sk > 70):
        return "skip"
    return prediction