import pandas as pd
from flask import Flask, render_template, request
import os

app = Flask(__name__)

data_directory = "/home/ec2-user/backtrader_app/data"

def load_data():
    processed_data_path = os.path.join(data_directory, "processed/TQQQ_break_out_results.csv")
    status_data_path = os.path.join(data_directory, "status/TQQQ_break_out_status.csv")

    processed_data = pd.read_csv(processed_data_path)
    status_data = pd.read_csv(status_data_path)

    return processed_data, status_data

@app.route('/')
def index():
    processed_data, status_data = load_data()
    return render_template("index.html", processed_data=processed_data.to_html(), status_data=status_data.to_html())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
