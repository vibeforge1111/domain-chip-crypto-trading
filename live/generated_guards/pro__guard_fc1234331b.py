def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    confirmations = 0
    if prediction == "long" and features.get("stoch_k", 50) < 25:
        confirmations += 1
    elif prediction == "short" and features.get("stoch_k", 50) > 75:
        confirmations += 1
    if prediction == "long" and features.get("vwap_deviation", 0) < 0:
        confirmations += 1
    elif prediction == "short" and features.get("vwap_deviation", 0) > 0:
        confirmations += 1
    if features.get("obv_slope", 0) > 0 and prediction == "long":
        confirmations += 1
    elif features.get("obv_slope", 0) < 0 and prediction == "short":
        confirmations += 1
    if features.get("macd_histogram", 0) > 0 and prediction == "long":
        confirmations += 1
    elif features.get("macd_histogram", 0) < 0 and prediction == "short":
        confirmations += 1
    if confirmations >= 2:
        return prediction
    return "skip"