from flask import Blueprint, render_template
import json
import plotly
import plotly.graph_objects as go
from blueprints.data_loader import load_data

plot_bp = Blueprint('plot_bp', __name__)


@plot_bp.route('/interactive_plot')
def interactive_plot():
    processed_data, _ = load_data()
    fig1 = break_out_figure(processed_data)
    graph_json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("interactive_plot.html", graph_json=graph_json)


def load_signal_data(processed_data, signal):
    date = processed_data.loc[processed_data['signal'] == signal, 'date']
    close = processed_data.loc[processed_data['signal'] == signal, 'close']
    return date, close


def break_out_figure(processed_data):
    # Setup Markers
    marker_offset = 10
    buy_date, buy_signal = load_signal_data(processed_data, 'BUY')
    sell_date, sell_signal = load_signal_data(processed_data, 'SELL')
    hold_date, hold_signal = load_signal_data(processed_data, 'HOLD')
    wait_date, wait_signal = load_signal_data(processed_data, 'WAIT')
    sell_signal += marker_offset
    buy_signal += marker_offset
    wait_signal += marker_offset
    hold_signal += marker_offset

    # Setup Data
    x = processed_data['date']
    y1 = processed_data['close']
    y2 = processed_data['hull_high']
    y3 = processed_data['tr']
    y4 = processed_data['atr']

    # Make Figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y1,
        mode='lines',
        name='Close'
        ))
    fig.add_trace(go.Scatter(
        x=x,
        y=y2,
        mode='lines',
        name='Hull High'
        ))
    fig.add_trace(go.Scatter(
        x=x,
        y=y3,
        mode='lines',
        name='TR'
        ))
    fig.add_trace(go.Scatter(
        x=x,
        y=y4,
        mode='lines',
        name='ATR'
        ))
    fig.add_trace(go.Scatter(
        x=buy_date,
        y=buy_signal,
        mode='markers',
        name='Buy',
        marker=dict(
            color='green',
            size=10)
        ))
    fig.add_trace(go.Scatter(
        x=sell_date,
        y=sell_signal,
        mode='markers',
        name='Sell',
        marker=dict(
            color='red',
            size=10)
        ))
    fig.add_trace(go.Scatter(
        x=hold_date,
        y=hold_signal,
        mode='markers',
        name='Hold',
        marker=dict(
            color='orange',
            size=3)
        ))
    fig.add_trace(go.Scatter(
        x=wait_date,
        y=wait_signal,
        mode='markers',
        name='Wait',
        marker=dict(
            color='yellow',
            size=3)
        ))
    fig.update_layout(
        title='Break Out Strategy',
        xaxis_title='Date',
        yaxis_title='Value'
        )
    return fig
