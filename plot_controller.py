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

    # Create a Plotly Figure
    fig = go.Figure()

    # Add the 'close' trace
    fig.add_trace(
        go.Scatter(x=processed_data['date'],
                   y=processed_data['close'],
                   mode='lines', name='Close'))

    # Add the 'tr', 'atr', and 'hull_high' traces
    fig.add_trace(
        go.Scatter(x=processed_data['date'],
                   y=processed_data['tr'],
                   mode='lines', name='TR'))
    fig.add_trace(go.Scatter(x=processed_data['date'],
                             y=processed_data['atr'],
                             mode='lines', name='ATR'))
    fig.add_trace(go.Scatter(x=processed_data['date'],
                             y=processed_data['hull_high'],
                             mode='lines', name='Hull High'))

    # Add the 'signal' trace
    fig.add_trace(go.Scatter(x=processed_data['date'],
                             y=processed_data['signal'],
                             mode='markers', name='Signal'))

    # Configure the layout
    fig.update_layout(title='Processed Data Plot',
                      xaxis_title='Date',
                      yaxis_title='Value')

    # Convert the figure to JSON
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return jsonify(graph_json)


def interactive_plot_js():
    return render_template("interactive_plot_js.html")
