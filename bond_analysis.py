import numpy as np
import numpy_financial as npf

def bond_analysis(face_value, coupon_rate, years_to_maturity, market_rate, payment_frequency=1, partial_capital_returns=None):
    periods = years_to_maturity * payment_frequency
    coupon_payment = (face_value * coupon_rate) / payment_frequency
    coupon_payments = np.full(periods, coupon_payment)

    if partial_capital_returns:
        # Adjust coupon payments for partial capital returns
        for year, amount in partial_capital_returns.items():
            index = year * payment_frequency - 1
            coupon_payments[index] += amount

    discount_factors = 1 / (1 + market_rate / payment_frequency) ** np.arange(1, periods + 1)

    present_value = np.sum(coupon_payments * discount_factors)

    cash_flows = np.full(periods, coupon_payment)

    if partial_capital_returns:
        # Adjust cash flows for partial capital returns
        for year, amount in partial_capital_returns.items():
            index = year * payment_frequency - 1
            cash_flows[index] += amount

    duration = np.sum(cash_flows * np.arange(1, periods + 1) / (1 + market_rate / payment_frequency)) / present_value

    modified_duration = duration / (1 + market_rate / payment_frequency)

    # Additional calculations
    from scipy.optimize import root

    cash_flow_function = lambda r: npf.npv(r / payment_frequency, cash_flows)
    result = root(cash_flow_function, x0=0.05)
    yield_to_call = result.x[0]
    yield_to_worst = min(yield_to_maturity, yield_to_call)

    npv = npf.npv(market_rate / payment_frequency, cash_flows)

    yield_to_maturity = npf.irr(cash_flows)

    current_yield = (coupon_payment * payment_frequency) / (face_value * (1 + market_rate / payment_frequency))

    macaulay_duration = np.sum(cash_flows * np.arange(1, periods + 1)) / present_value

    convexity = np.sum(cash_flows * np.arange(1, periods + 1) * np.arange(1, periods + 1) /
                      (1 + market_rate / payment_frequency) ** (2 * np.arange(1, periods + 1))) / present_value

    modified_convexity = convexity / (1 + market_rate / payment_frequency)

    pvbp = convexity * (0.01 / payment_frequency)

    return {
        "Duration": duration,
        "Modified Duration": modified_duration,
        "IRR": yield_to_maturity,
        "NPV": npv,
        "Yield to Maturity": yield_to_maturity,
        "Current Yield": current_yield,
        "Yield to Call": yield_to_call,
        "Yield to Worst": yield_to_worst,
        "Macaulay Duration": macaulay_duration,
        "Convexity": convexity,
        "Modified Convexity": modified_convexity,
        "Price Value of a Basis Point": pvbp
    }

# Example usage:
face_value = 1000
coupon_rate = 0.05
years_to_maturity = 5
market_rate = 0.04
payment_frequency = 1
partial_capital_returns = {3: 50, 4: 50}  # Example: Partial capital returns in years 3 and 4

result = bond_analysis(face_value, coupon_rate, years_to_maturity, market_rate, payment_frequency, partial_capital_returns)
print(result)
