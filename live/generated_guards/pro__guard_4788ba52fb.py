def guard(features: dict, prediction: str) -> str:
    sk, sd = features["stoch_k"], features["stoch_d"]
    if prediction == "long":
        if sk > sd and sd < 30 and sk < 70:
            return prediction
    elif prediction == "short":
        if sk < sd and sd > 70 and sk > 30:
            return prediction
    return "skip"