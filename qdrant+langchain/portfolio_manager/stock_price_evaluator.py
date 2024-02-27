import yfinance as yf
from datetime import datetime, timedelta

from portfolio_constants import portfolio

def get_daily_price_performance(company_name):
    portfolio_stock = None
    for entry in portfolio:
        if entry["company_name"] == company_name:
            portfolio_stock = entry
            break

    stock_symbol = portfolio_stock["ticker"]
    today = datetime.now()  # Get today's date
    start_date = today - timedelta(days=4)  # Calculate the start date
    start_date_str = start_date.strftime('%Y-%m-%d')

    end_date_str = today.strftime('%Y-%m-%d')

    # Fetch stock data for the given ticker
    stock_data = yf.download(stock_symbol, start=start_date_str, end=end_date_str)

    if not stock_data.empty:
        current_close_price = stock_data['Close'][-1]
        previous_close_price = stock_data['Close'][-2]

        daily_profit_loss = current_close_price - previous_close_price
        profit_loss_percentage = (daily_profit_loss / previous_close_price) * 100

        if daily_profit_loss > 0:
            return f"{stock_symbol} Went up by {profit_loss_percentage:.2f} % in the last trading session"
        elif daily_profit_loss < 0:
            return f"{stock_symbol} Went down {abs(profit_loss_percentage):.2f} % in the last trading session"
        else:
            return "No change in the stock price in the last trading session"
    else:
        print(f"No data available for {stock_symbol} on {end_date_str}")
