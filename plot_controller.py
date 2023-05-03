from flask import render_template, jsonify
import plotly
import plotly.graph_objects as go
import json
from data_loader import load_data


def register_routes(app):
    app.add_url_rule('/interactive_plot', 'interactive_plot', interactive_plot)
    app.add_url_rule('/interactive_plot_js', 'interactive_plot_js',
                     interactive_plot_js)


def interactive_plot():
    processed_data, _ = load_data()
    date = processed_data['date']
    buy_date = processed_data.loc[
        processed_data['signal'] == 'BUY', 'date']
    buy_signal = processed_data.loc[
        processed_data['signal'] == 'BUY', 'close']
    sell_date = processed_data.loc[
        processed_data['signal'] == 'SELL', 'date']
    sell_signal = processed_data.loc[
        processed_data['signal'] == 'SELL', 'close']
    hold_date = processed_data.loc[
        processed_data['signal'] == 'HOLD', 'date']
    hold_signal = processed_data.loc[
        processed_data['signal'] == 'HOLD', 'close']

    # Create the first Plotly Figure for close and hull_high
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=date,
                              y=processed_data['close'],
                              mode='lines', name='Close'))
    fig1.add_trace(go.Scatter(x=date,
                              y=processed_data['hull_high'],
                              mode='lines', name='Hull High'))
    fig1.add_trace(go.Scatter(x=buy_date,
                              y=buy_signal,
                              mode='markers', name='Buy',
                              marker=dict(color='green', size=10)))

    fig1.add_trace(go.Scatter(x=sell_date,
                              y=sell_signal,
                              mode='markers', name='Sell',
                              marker=dict(color='red', size=10)))

    fig1.add_trace(go.Scatter(x=hold_date,
                              y=hold_signal,
                              mode='markers', name='Hold',
                              marker=dict(color='orange', size=5)))

    fig1.update_layout(title='Close and Hull High Plot',
                       xaxis_title='Date',
                       yaxis_title='Value')

    # Create the second Plotly Figure for tr and atr
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=processed_data['date'],
                              y=processed_data['tr'],
                              mode='lines', name='TR'))
    fig2.add_trace(go.Scatter(x=processed_data['date'],
                              y=processed_data['atr'],
                              mode='lines', name='ATR'))
    fig2.update_layout(title='TR and ATR Plot',
                       xaxis_title='Date', yaxis_title='Value')

    # Convert both figures to JSON
    graph1_json = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph2_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify({'graph1': graph1_json, 'graph2': graph2_json})


def interactive_plot_js():
    return render_template("interactive_plot_js.html")
