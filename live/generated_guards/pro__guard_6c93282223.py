def guard(features: dict, prediction: str) -> str:
    # Skip if momentum is decelerating (macd_histogram near zero) while overbought
    if -0.0001 < features.get('macd_histogram', 0) < 0.0001 and features.get('rsi_2h', 50) > 70:
        return "skip"
    return prediction