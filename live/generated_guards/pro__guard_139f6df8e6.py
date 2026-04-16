def guard(features: dict, prediction: str) -> str:
    if prediction == "long" and features["stoch_k"] <= features["stoch_d"]:
        return "skip"
    if prediction == "short" and features["stoch_k"] >= features["stoch_d"]:
        return "skip"
    return prediction