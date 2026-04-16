def guard(features: dict, prediction: str) -> str:
    # True compression: low volatility with no conflicting signals
    is_compressed = features.get('atr_ratio', 1) < 0.5 and features.get('bb_width', 0.5) < 0.3
    
    if is_compressed and prediction != "skip":
        # False compression: extreme stochastics in compressed state
        if features.get('stoch_k', 50) < 20 or features.get('stoch_k', 50) > 80:
            return "skip"
        
        # False compression: VWAP far from price during compression breakout
        if abs(features.get('vwap_deviation', 0)) > 0.02:
            return "skip"
        
        # False compression: conflicting RSI 2h context
        rsi_2h = features.get('rsi_2h', 50)
        if (prediction == "long" and rsi_2h > 70) or (prediction == "short" and rsi_2h < 30):
            return "skip"
        
        # False compression: MACD histogram opposing prediction
        macd = features.get('macd_histogram', 0)
        if (prediction == "long" and macd < -0.001) or (prediction == "short" and macd > 0.001):
            return "skip"
    
    return prediction