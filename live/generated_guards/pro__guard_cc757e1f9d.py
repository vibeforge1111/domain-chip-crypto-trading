def guard(features: dict, prediction: str) -> str:
    """Filter trades when momentum is decelerating."""
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    obv = features.get('obv_slope', 0)
    
    # Skip if macd histogram negative (momentum weakening) AND stoch overbought
    if macd < 0 and stoch > 80:
        return "skip"
    # Skip if negative macd with negative obv slope (distribution)
    if macd < 0 and obv < 0:
        return "skip"
    return prediction