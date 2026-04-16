def guard(features: dict, prediction: str) -> str:
    obv = features['obv_slope']
    stoch = features['stoch_k']
    macd = features['macd_histogram']
    # Skip longs when OBV shows distribution (selling pressure)
    if obv < -0.05 and prediction == 'long':
        return 'skip'
    # Skip shorts when OBV shows accumulation (buying pressure)
    if obv > 0.05 and prediction == 'short':
        return 'skip'
    # Skip longs when stoch overbought (reversal likely)
    if stoch > 75 and prediction == 'long':
        return 'skip'
    # Skip shorts when stoch oversold (bounce likely)
    if stoch < 25 and prediction == 'short':
        return 'skip'
    return prediction