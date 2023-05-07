from flask import render_template, jsonify
import plotly
import plotly.graph_objects as go
import json
from data_loader import load_data


def register_routes(app):
    app.add_url_rule('/interactive_plot', 'interactive_plot', interactive_plot)
    app.add_url_rule('/interactive_plot_js', 'interactive_plot_js',
                     interactive_plot_js)


def load_signal_data(processed_data, signal):
    date = processed_data.loc[processed_data['signal'] == signal, 'date']
    close = processed_data.loc[processed_data['signal'] == signal, 'close']
    return date, close


def create_close_hull_high_figure(processed_data, buy_date, buy_signal,
                                  sell_date, sell_signal, hold_date,
                                  hold_signal, wait_date, wait_signal):
    date = processed_data['date']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=processed_data['close'],
                             mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=date, y=processed_data['hull_high'],
                             mode='lines', name='Hull High'))
    fig.add_trace(go.Scatter(x=buy_date, y=buy_signal+10,
                             mode='markers', name='Buy',
                             marker=dict(color='green', size=10)))
    fig.add_trace(go.Scatter(x=sell_date, y=sell_signal+10,
                             mode='markers', name='Sell',
                             marker=dict(color='red', size=10)))
    fig.add_trace(go.Scatter(x=hold_date, y=hold_signal+10,
                             mode='markers', name='Hold',
                             marker=dict(color='orange', size=3)))
    fig.add_trace(go.Scatter(x=wait_date, y=wait_signal+10,
                             mode='markers', name='Wait',
                             marker=dict(color='yellow', size=3)))
    fig.update_layout(title='Close and Hull High Plot',
                      xaxis_title='Date',
                      yaxis_title='Value')
    return fig


def create_tr_atr_figure(processed_data):
    date = processed_data['date']
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=processed_data['tr'],
                             mode='lines', name='TR'))
    fig.add_trace(go.Scatter(x=date, y=processed_data['atr'],
                             mode='lines', name='ATR'))
    fig.update_layout(title='TR and ATR Plot', xaxis_title='Date',
                      yaxis_title='Value')
    return fig


def interactive_plot():
    processed_data, _ = load_data()

    buy_date, buy_signal = load_signal_data(processed_data, 'BUY')
    sell_date, sell_signal = load_signal_data(processed_data, 'SELL')
    hold_date, hold_signal = load_signal_data(processed_data, 'HOLD')
    wait_date, wait_signal = load_signal_data(processed_data, 'WAIT')

    fig1 = create_close_hull_high_figure(processed_data, buy_date, buy_signal,
                                         sell_date, sell_signal, hold_date,
                                         hold_signal, wait_date, wait_signal)
    fig2 = create_tr_atr_figure(processed_data)

    graph1_json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({'graph1': graph1_json, 'graph2': graph2_json})


def interactive_plot_js():
    # test comment
    return render_template("interactive_plot_js.html")
