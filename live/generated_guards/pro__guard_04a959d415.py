def guard(features: dict, prediction: str) -> str:
    # True compression: both ATR and Bollinger width must be low
    is_compressed = features.get('atr_ratio', 1.0) < 0.7 and features.get('bb_width', 0.5) < 0.3
    
    if is_compressed and prediction != 'skip':
        # False compression detected when momentum contradicts prediction
        macd = features.get('macd_histogram', 0)
        obv = features.get('obv_slope', 0)
        
        if prediction == 'long' and (macd < 0 or obv < 0):
            return 'skip'
        if prediction == 'short' and (macd > 0 or obv > 0):
            return 'skip'
        
        # Extreme stoch + large VWAP deviation = likely false break
        stoch_k = features.get('stoch_k', 50)
        vwap_dev = features.get('vwap_deviation', 0)
        
        if abs(stoch_k - 50) > 30 and abs(vwap_dev) > 0.003:
            return 'skip'
    
    return prediction