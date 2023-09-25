import os
import pandas as pd

data_directory = "../backtrader_app/data"


def load_data():
    processed_data_path = os.path.join(
        data_directory, "processed/TQQQ_algo_1_results.csv")
    status_data_path = os.path.join(
        data_directory, "status/TQQQ_algo_1_status.csv")

    processed_data = pd.read_csv(processed_data_path)
    status_data = pd.read_csv(status_data_path)

    return processed_data, status_data
