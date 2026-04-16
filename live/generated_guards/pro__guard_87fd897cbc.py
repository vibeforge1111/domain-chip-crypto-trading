def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    long_signals = (
        (features.get('rsi_14', 50) < 70) +
        (features.get('stoch_k', 50) < 80) +
        (features.get('vwap_deviation', 0) < 0) +
        (features.get('bb_pct_b', 0.5) < 0.5) +
        (features.get('macd_histogram', 0) > 0) +
        (features.get('obv_slope', 0) > 0)
    )
    
    short_signals = (
        (features.get('rsi_14', 50) > 30) +
        (features.get('stoch_k', 50) > 20) +
        (features.get('vwap_deviation', 0) > 0) +
        (features.get('bb_pct_b', 0.5) > 0.5) +
        (features.get('macd_histogram', 0) < 0) +
        (features.get('obv_slope', 0) < 0)
    )
    
    return "skip" if (prediction == "long" and long_signals < 2) or (prediction == "short" and short_signals < 2) else prediction