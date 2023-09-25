from flask import Flask
from blueprints.plot_controller_1 import plot_bp_1
from blueprints.status_controller_1 import status_bp_1
from blueprints.plot_controller_2 import plot_bp_2
from blueprints.status_controller_2 import status_bp_2
from blueprints.homepage import home_bp

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.register_blueprint(home_bp)
app.register_blueprint(status_bp_1)
app.register_blueprint(plot_bp_1)
app.register_blueprint(status_bp_2)
app.register_blueprint(plot_bp_2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
