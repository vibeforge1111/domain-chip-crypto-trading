def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    count = 0
    if prediction == "long":
        if features.get("rsi_14", 50) < 65: count += 1
        if features.get("vwap_deviation", 0) > 0: count += 1
        if features.get("macd_histogram", 0) > 0: count += 1
        if features.get("rsi_2h", 50) > 45: count += 1
    else:
        if features.get("rsi_14", 50) > 35: count += 1
        if features.get("vwap_deviation", 0) < 0: count += 1
        if features.get("macd_histogram", 0) < 0: count += 1
        if features.get("rsi_2h", 50) < 55: count += 1
    if count < 2:
        return "skip"
    return prediction