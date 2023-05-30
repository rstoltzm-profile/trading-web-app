from flask import Blueprint, render_template
import plotly.graph_objects as go
from blueprints.data_loader import load_data
from datetime import timedelta, datetime


plot_bp = Blueprint('plot_bp', __name__)


@plot_bp.route('/interactive_plot')
def interactive_plot():
    processed_data, _ = load_data()
    fig1 = break_out_figure(processed_data)
    fig1 = add_buttons_figure(fig1)
    fig2 = break_out_figure2(processed_data)
    fig2 = add_buttons_figure(fig2)
    fig3 = break_out_figure3(processed_data)
    fig3 = add_buttons_figure(fig3)
    with open('./templates/break_out_graph.html', 'w') as f:
        f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
    return render_template("break_out_graph.html")


def load_signal_data(processed_data, signal):
    date = processed_data.loc[processed_data['signal'] == signal, 'date']
    close = processed_data.loc[processed_data['signal'] == signal, 'close']
    return date, close


def add_buttons_figure(fig):
    fig.update_layout(
        width=600,
        height=400,
    )
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(
                        label="Last 14 days",
                        method="relayout",
                        args=[{"xaxis.range": [
                            datetime.now() - timedelta(days=14), datetime.now()
                            ]}]),
                    dict(
                        label="Last 30 days",
                        method="relayout",
                        args=[{"xaxis.range": [
                            datetime.now() - timedelta(days=30), datetime.now()
                            ]}]),
                    dict(
                        label="Last 90 days",
                        method="relayout",
                        args=[{"xaxis.range": [
                            datetime.now() - timedelta(days=90), datetime.now()
                            ]}]),
                ]),
                type="buttons",
                direction="right",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.25,
                xanchor="left",
                y=1.25,
                yanchor="top"
            )
        ])
    return fig


def break_out_figure(processed_data):
    # Setup Markers
    buy_date, buy_signal = load_signal_data(processed_data, 'BUY')
    sell_date, sell_signal = load_signal_data(processed_data, 'SELL')
    hold_date, hold_signal = load_signal_data(processed_data, 'HOLD')
    wait_date, wait_signal = load_signal_data(processed_data, 'WAIT')

    # Setup Data
    x = processed_data['date']
    y1 = processed_data['close']
    y2 = processed_data['hull_high']

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
        x=buy_date,
        y=buy_signal,
        mode='markers',
        name='Buy',
        marker=dict(
            color='green',
            size=10,
            symbol='triangle-up',
            standoff=5)
        ))
    fig.add_trace(go.Scatter(
        x=sell_date,
        y=sell_signal,
        mode='markers',
        name='Sell',
        marker=dict(
            color='red',
            size=10,
            symbol='triangle-down')
        ))
    fig.add_trace(go.Scatter(
        x=hold_date,
        y=hold_signal,
        mode='markers',
        name='Hold',
        marker=dict(
            color='orange',
            size=5,
            symbol='line-ns',
            line_width=1.5,
            line=dict(
                color='orange',
                width=1.5))
        ))
    fig.add_trace(go.Scatter(
        x=wait_date,
        y=wait_signal,
        mode='markers',
        name='Wait',
        marker=dict(
            color='blue',
            size=5,
            symbol='line-ns',
            line_width=1.5,
            line=dict(
                color='blue',
                width=1.5))
        ))
    fig.update_layout(
        title='Break Out Strategy',
        xaxis_title='Date',
        yaxis_title='Value',
        )
    return fig


def break_out_figure2(processed_data):

    # Setup Data
    x = processed_data['date']
    y3 = processed_data['tr']
    y4 = processed_data['atr']
    y = y3 - y4

    # Make Figure
    fig = go.Figure()
    fig.add_hline(y=0, line_width=1, line_color="red")
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='value'
        ))
    fig.update_layout(
        title='TR - ATR',
        xaxis_title='Date',
        yaxis_title='Value',
        width=600,
        height=500,
        )
    return fig


def break_out_figure3(processed_data):

    # Setup Data
    x = processed_data['date']
    y3 = processed_data['close']
    y4 = processed_data['hull_high']
    y = y3-y4

    # Make Figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Value'
        ))
    fig.add_hline(y=0, line_width=1, line_color="red")
    fig.update_layout(
        title='Close - Hull High',
        xaxis_title='Date',
        yaxis_title='Value',
        width=600,
        height=500,
        )
    return fig
