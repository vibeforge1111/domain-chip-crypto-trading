def guard(features: dict, prediction: str) -> str:
    # Reject extended price with exhausted momentum (mean reversion trap)
    # When price reaches extreme BB position AND RSI is overbought/oversold,
    # the signal is likely to reverse rather than continue
    bb_pos = features.get('bb_position', 0.5)
    rsi = features.get('rsi_14', 50)
    
    if prediction == 'long' and bb_pos > 0.92 and rsi > 72:
        return "skip"
    if prediction == 'short' and bb_pos < 0.08 and rsi < 28:
        return "skip"
    
    return prediction