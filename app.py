from flask import Flask, render_template
from plot_controller import register_routes
from data_loader import load_data

app = Flask(__name__)

register_routes(app)


@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/status')
def status():
    _, status_data = load_data()
    return render_template("status.html", status_data=status_data.to_html())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
