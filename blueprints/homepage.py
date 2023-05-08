from flask import Blueprint, render_template

home_bp = Blueprint('homepage', __name__)


@home_bp.route('/')
def login():
    return render_template("login.html")


@home_bp.route('/home')
def homepage():
    return render_template("homepage.html")
