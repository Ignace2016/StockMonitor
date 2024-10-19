from flask import Flask, render_template
import yfinance as yf
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

# Dictionary of stock symbols
stock_dict = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Nvidia': 'NVDA',
    'Tesla': 'TSLA',
    'Uber': 'UBER',
    'Expedia': 'EXPE',
    'Netflix': 'NFLX',
    'Google': 'GOOG',
    'Costco': 'COST',
    'VOO': 'VOO'
}

# Function to fetch stock data for a given period
def fetch_stock_data(stock_symbol, period='5y'):
    df = yf.Ticker(stock_symbol).history(period=period)
    return df

# Function to generate a Plotly graph for a given stock
def plot_stock(stock_name, df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index, 
        y=df['Close'], 
        mode='lines', 
        line=dict(color='green'), 
        fill='tozeroy',  
        fillcolor='rgba(0, 128, 0, 0.2)'  
    ))

    fig.update_layout(
        title={
            'text': f'{stock_name}',
            'x': 0.5,  # Center the title
            'xanchor': 'center'
        },
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        margin=dict(l=40, r=40, t=40, b=40),  # Adjust margins
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, gridcolor='lightgray'),  
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        autosize=True  # Make sure Plotly graph resizes dynamically
    )

    return pio.to_json(fig)


# Main route to render the page and graphs
@app.route('/')
def index():
    stock_graphs = {}
    for stock_name, stock_symbol in stock_dict.items():
        df = fetch_stock_data(stock_symbol)
        graph_json = plot_stock(stock_name, df)
        stock_graphs[stock_name] = graph_json
    
    return render_template('index.html', stock_graphs=stock_graphs)

if __name__ == '__main__':
    app.run(debug=True)
