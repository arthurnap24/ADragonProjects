
# calculate the number of shares to buy and the stop price and take profit price
def calculate_share_info( share_price, capital, risk, gain_multiplier ):
    total_shares = float(capital) / share_price
    risk_decimal = float(risk) / 100
    risk_amount = capital * risk_decimal
    gain_amount = risk_amount * gain_multiplier
    
    stop_price = share_price - (risk_amount / total_shares)
    take_profit = share_price + (gain_amount / total_shares)

    return {
        "num_shares": str(total_shares),
        "risk_amount": str(risk_amount),
        "gain_amount": str(gain_amount),
        "stop_price": str(stop_price),
        "take_profit": str(take_profit)
    }