from flask import Flask, send_file
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import io
app = Flask(__name__)

@app.route('/', methods = ['GET'])
def stock_grap():
    import pandas as pd
    import yfinance as yf
    import matplotlib.pyplot as plt
    import io

    start_date = '2022-01-01'
    end_date = '2024-8-31'

    stock_code = '035420.KS'

    moving_average_periods = [20, 40, 60]
    _20_days_period = 20
    _40_days_period = 40
    _60_days_period = 60

    data = yf.download(stock_code, start=start_date, end=end_date)

    data['_20_MA'] = data['Close'].rolling(window=_20_days_period).mean()
    data['_40_MA'] = data['Close'].rolling(window=_40_days_period).mean()
    data['_60_MA'] = data['Close'].rolling(window=_60_days_period).mean()

    data['Buy_Signal'] = False
    data.loc[
        (data['_20_MA'] > data['_40_MA']) &
        (data['_40_MA'] > data['_60_MA']).shift() &
        (data['_60_MA'] ==
    data['_60_MA'].rolling(window=_60_days_period).max()),
        'Buy_Signal'
    ] = True

    buy = []
    sell = []
    def chkCross(data):
        chk = 0
        for i in range(len(data)):
            buy.append(False)
            sell.append(False)
            if data['_60_MA'][i] < data['_40_MA'][i] and data['_40_MA'][i] < data['_20_MA'][i] and chk == 0:
                print('Golden cross ', str(data.index[i])[:10])
                chk = 1
                buy[i] = True
            elif data['_60_MA'][i] > data['_40_MA'][i] and data['_40_MA'][i] > data['_20_MA'][i] and chk == 1:
                print('Death cross ', str(data.index[i])[:10])
                chk = 0
                sell[i] = True
    chkCross(data)            
                
    data['buy'] = buy
    data['sell'] = sell

    plt.rc('font', family = 'Malgun Gothic')
    plt.figure(figsize=(12, 8))
    plt.plot(data['Close'], label='종가')
    plt.plot(data['_20_MA'], label=f'{_20_days_period}일선')
    plt.plot(data['_40_MA'], label=f'{_40_days_period}일선')
    plt.plot(data['_60_MA'], label=f'{_60_days_period}일선')

    plt.plot(data._60_MA[data.buy == True], '^', markersize=10, color='r', label="Golden")
    plt.plot(data._60_MA[data.sell == True], 'v', markersize=10, color='b', label="Death")

    buy_dates = data[data['Buy_Signal']].index
    buy_prices = data[data['Buy_Signal']]['Close']

    plt.title('Nexon Stock Price with Moving Averages and Buy Signals')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.legend()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    return send_file(img, mimetype='image/png', as_attachment=False, download_name='stock_plot.png')

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)