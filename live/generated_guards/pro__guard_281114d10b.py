def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish = sum([features["bb_pct_b"] < 0.25, features["vwap_deviation"] > 0,
                   features["stoch_k"] > 55, features["obv_slope"] > 0,
                   features["macd_histogram"] > 0, features["rsi_2h"] > 55])
    bearish = sum([features["bb_pct_b"] > 0.75, features["vwap_deviation"] < 0,
                   features["stoch_k"] < 45, features["obv_slope"] < 0,
                   features["macd_histogram"] < 0, features["rsi_2h"] < 45])
    
    return prediction if (prediction == "long" and bullish >= 2) or (prediction == "short" and bearish >= 2) else "skip"