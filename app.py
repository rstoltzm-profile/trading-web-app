from flask import Flask, render_template
from blueprints.plot_controller import plot_bp
from blueprints.status_controller import status_bp

app = Flask(__name__)

app.register_blueprint(status_bp)
app.register_blueprint(plot_bp)


@app.route('/')
def homepage():
    return render_template("homepage.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
