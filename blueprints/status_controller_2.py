from flask import Blueprint, render_template
from blueprints.data_loader_2 import load_data

status_bp_2 = Blueprint('status_2', __name__)


@status_bp_2.route('/status_2')
def status():
    _, status_data = load_data()
    status_data = status_data[['strategy','last_signal', 'last_signal_date', 'data_status', 'last job time', 'percent_profit', 'drawdown', 'algo_start', 'live_start_date', 'live_start_funds']]
    status_data = status_data.rename(
        columns={'strategy': 'Strategy',
                 'data_status': 'Latest Stock Data',
                 'last_signal': 'Latest Signal',
                 'last_signal_date': 'Latest Signal Date',
                 'percent_profit': 'Profit %',
                 'drawdown': 'Drawdown %',
                 'algo_start': 'Algo Data Start',
                 'live_start_date': 'Live Start Date',
                 'live_start_funds': 'Live Cash',
                 'last job time': 'Latest Job Run',
                 }
        )
    status_data = status_data.iloc[0]
    status_data = status_data.to_frame().reset_index()
    status_data.columns = ['column_name', 'value']
    return render_template("status.html", table=status_data)
