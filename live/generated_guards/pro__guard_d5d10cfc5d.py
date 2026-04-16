def guard(features: dict, prediction: str) -> str:
    # True compression: narrow bb_width + price in middle of bands + low ATR
    is_compressed = features.get('bb_width', 1) < 0.12
    is_mid_band = 0.35 < features.get('bb_pct_b', 0.5) < 0.65
    low_volatility = features.get('atr_ratio', 1) < 0.8
    near_vwap = abs(features.get('vwap_deviation', 0)) < 0.005
    
    true_compression = is_compressed and is_mid_band and low_volatility and near_vwap
    
    # False compression warnings: stoch divergence, rsi_2h mismatch
    stoch_div = abs(features.get('stoch_k', 50) - features.get('stoch_d', 50)) > 18
    rsi_2h = features.get('rsi_2h', 50)
    rsi_mismatch = (prediction == "long" and rsi_2h > 72) or (prediction == "short" and rsi_2h < 28)
    
    if true_compression and (stoch_div or rsi_mismatch):
        return "skip"
    
    return prediction