def guard(features: dict, prediction: str) -> str:
    # Skip if momentum is decelerating (negative MACD histogram)
    # Combined with stochastic overbought/oversold to catch reversals
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    
    if prediction == "long" and macd < 0 and stoch > 80:
        return "skip"
    if prediction == "short" and macd < 0 and stoch < 20:
        return "skip"
    return prediction