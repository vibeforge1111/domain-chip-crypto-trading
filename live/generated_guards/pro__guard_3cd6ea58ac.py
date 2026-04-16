def guard(features: dict, prediction: str) -> str:
    # Detect momentum deceleration using MACD histogram
    macd = features.get('macd_histogram', 0)
    rsi = features.get('rsi_14', 50)
    
    # Skip if momentum is weakening (negative histogram)
    if macd < -0.0001:
        # Confirm with RSI extreme for stronger signal
        if rsi > 70 or rsi < 30:
            return "skip"
    return prediction