from flask import Blueprint, render_template
from blueprints.data_loader import load_data

status_bp = Blueprint('status', __name__)


@status_bp.route('/status')
def status():
    _, status_data = load_data()
    return render_template("status.html", status_data=status_data.to_html())
