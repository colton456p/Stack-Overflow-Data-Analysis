import os

import matplotlib.pyplot as plt
import seaborn as sns


def save_graph(figure_file_name: str, format: str, post_LLM: bool):
    configured_file = figure_file_name + "." + format
    if post_LLM:
        graph_type = "post_LLM_graphs"
    else:
        graph_type = "pre_LLM_graphs"
    try:
        plt.savefig(f"src/graphs/{graph_type}/{configured_file}", format=format)
    except FileNotFoundError:
        os.makedirs(f"src/graphs/{graph_type}", exist_ok=True)
        plt.savefig(f"src/graphs/{graph_type}/{configured_file}", format=format)


def save_comparison_graph(figure_file_name, format):
    configured_file = figure_file_name + "." + format
    try:
        plt.savefig(f"src/graphs/comparison_graphs/{configured_file}", format=format)
    except FileNotFoundError:
        os.makedirs(f"src/graphs/comparison_graphs", exist_ok=True)
        plt.savefig(f"src/graphs/comparison_graphs/{configured_file}", format=format)


def reset_graph_settings():
    """
    Reset all settings for matplotlib, seaborn, pandas, and numpy after graph generation
    """
    plt.rcdefaults()
    sns.reset_defaults()
    plt.clf()
    plt.close()


def convert_hours(hour_str):
    hour = int(hour_str.split(":")[0])
    if hour == 0:
        return "12 AM"
    elif hour < 12:
        return f"{hour} AM"
    elif hour == 12:
        return "12 PM"
    else:
        return f"{hour - 12} PM"


def convert_hours_in_df(df):
    """
    Convert all 24-hour format columns in the DataFrame to 12-hour AM/PM format.
    """

    hour_columns = df.columns
    df.columns = [convert_hours(col) for col in hour_columns]

    return df


def create_graph(
    download_data: bool, figure_file_name: str, format: str, post_LLM: bool
):
    if download_data:
        save_graph(figure_file_name=figure_file_name, format=format, post_LLM=post_LLM)
    else:
        plt.show()
    reset_graph_settings()


def create_comparison_graph(download_data: bool, figure_file_name: str, format: str):
    if download_data:
        save_comparison_graph(figure_file_name=figure_file_name, format=format)
    else:
        plt.show()
    reset_graph_settings()
