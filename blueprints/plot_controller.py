from flask import Blueprint, render_template
import plotly.graph_objects as go
from blueprints.data_loader import load_data
from datetime import timedelta, datetime
from plotly.subplots import make_subplots


plot_bp = Blueprint('plot_bp', __name__)


@plot_bp.route('/interactive_plot')
def interactive_plot():
    processed_data, _ = load_data()
    fig1 = break_out_figure(processed_data)
    fig1 = add_buttons_figure(fig1)
    with open('./templates/break_out_graph.html', 'w') as f:
        f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    return render_template("break_out_graph.html")


def load_signal_data(processed_data, signal):
    date = processed_data.loc[processed_data['signal'] == signal, 'date']
    close = processed_data.loc[processed_data['signal'] == signal, 'close']
    return date, close


def add_buttons_figure(fig):
    fig.update_xaxes(
        showgrid=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='#444',
    )
    fig.update_yaxes(
        showgrid=False,
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='#444',
    )
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgb(234,242,250)',
        autosize=False,
        minreducedwidth=500,
        minreducedheight=300,
        width=600,
        height=800,
        legend=dict(
            yanchor="middle",
            y=0.5,
            xanchor="right",
            x=2,
        )
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
                    dict(
                        label="Reset",
                        method="relayout",
                        args=[{"xaxis.autorange": True
                            }]),
                ]),
                type="buttons",
                direction="left",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
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

    y_buy1 = y1-y2
    y3 = processed_data['tr']
    y4 = processed_data['atr']
    y_buy2 = y3 - y4
    y_sum = y_buy1+y_buy2

    # Make Figure
    # fig = go.Figure()
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        shared_yaxes=False,
        vertical_spacing=0.07,
        x_title='Date',
        subplot_titles=('BreakOut Algo',  'Buy Signals')
    )
    fig.add_scatter(
        x=x,
        y=y1,
        mode='lines',
        name='Close',
        row=1, col=1,
        legendgroup = '1'
        )
    fig.add_scatter(
        x=x,
        y=y2,
        mode='lines',
        name='Hull High',
        row=1, col=1,
        legendgroup = '1'
        )
    fig.add_scatter(
        x=buy_date,
        y=buy_signal,
        mode='markers',
        name='Buy',
        row=1, col=1,
        marker=dict(
            color='green',
            size=10,
            symbol='triangle-up')
        )
    fig.add_scatter(
        x=sell_date,
        y=sell_signal,
        mode='markers',
        name='Sell',
        row=1, col=1,
        marker=dict(
            color='red',
            size=10,
            symbol='triangle-down')
        )
    fig.add_scatter(
        x=hold_date,
        y=hold_signal,
        mode='markers',
        name='Hold',
        row=1, col=1,
        marker=dict(
            color='orange',
            size=5,
            symbol='line-ns',
            line_width=1.5,
            line=dict(
                color='orange',
                width=1.5))
        )
    fig.add_scatter(
        x=wait_date,
        y=wait_signal,
        mode='markers',
        name='Wait',
        row=1, col=1,
        marker=dict(
            color='blue',
            size=5,
            symbol='line-ns',
            line_width=1.5,
            line=dict(
                color='blue',
                width=1.5))
        )
    fig.add_scatter(
        x=x,
        y=y_buy1,
        mode='markers',
        name='signal 1',
        fill='tonexty',
        legendgroup = '2',
        #stackgroup='one',
        row=2, col=1
        )
    fig.add_scatter(
        x=x,
        y=y_buy2,
        mode='markers',
        name='signal 2',
        fill='tonexty',
        #stackgroup='one',
        row=2, col=1
        )
    fig.add_hline(y=0, row=2, col=1, line_width=1, line_color="green")
    return fig

