from flask import Flask
from blueprints.plot_controller import plot_bp
from blueprints.status_controller import status_bp
from blueprints.homepage import home_bp

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(status_bp)
app.register_blueprint(plot_bp)
app.register_blueprint(home_bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
