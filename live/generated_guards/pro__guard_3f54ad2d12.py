def guard(features: dict, prediction: str) -> str:
    obv = features.get("obv_slope", 0)
    vwap = features.get("vwap_deviation", 0)
    
    if prediction == "long" and (obv < 0 or vwap < 0):
        return "skip"
    if prediction == "short" and (obv > 0 or vwap > 0):
        return "skip"
    return prediction