def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish = sum([
        features["stoch_k"] < 25,
        features["vwap_deviation"] > 0.003,
        features["macd_histogram"] > 0,
        features["rsi_2h"] < 45,
        features["bb_pct_b"] < 0.25
    ])
    bearish = sum([
        features["stoch_k"] > 75,
        features["vwap_deviation"] < -0.003,
        features["macd_histogram"] < 0,
        features["rsi_2h"] > 55,
        features["bb_pct_b"] > 0.75
    ])
    
    confirm = bullish if prediction == "long" else bearish
    return "skip" if confirm < 2 else prediction