def guard(features: dict, prediction: str) -> str:
    # True compression: BB width and ATR both low
    compressed = features.get('bb_width', 1) > 0.5 and features.get('atr_ratio', 1) > 1.2
    
    if not compressed and prediction != 'skip':
        bb_pct = features.get('bb_pct_b', 0.5)
        vwap_dev = features.get('vwap_deviation', 0)
        stoch = features.get('stoch_k', 50)
        rsi_2h = features.get('rsi_2h', 50)
        
        # Long setup: price near lower band, below VWAP, oversold, 2h neutral/bullish
        if prediction == 'long':
            if bb_pct > 0.6 or vwap_dev > 0.01 or stoch > 75 or rsi_2h > 70:
                return 'skip'
        
        # Short setup: price near upper band, above VWAP, overbought, 2h neutral/bearish
        elif prediction == 'short':
            if bb_pct < 0.4 or vwap_dev < -0.01 or stoch < 25 or rsi_2h < 30:
                return 'skip'
    
    return prediction