import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def avg_posts_ph(
    download_data: bool = False,
    format: str = "png",
    csv_file: str = None,
    post_LLM: bool = None,
):
    """
    The file processed contains the average number of posts per hour.
    """
    if post_LLM is None:
        raise ValueError("Please provide a value for the post_LLM parameter.")
    try:
        df = pd.read_csv(f"CSV_files/{csv_file}", index_col=0)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Please provide a valid CSV file path. The file {csv_file} was not found in the CSV_files directory."
        )

    # Remove the first row of the dataframe which is simply the row numbers
    df = df.drop(df.columns[0], axis=1)
    df = np.floor(df).astype(int)
    df = convert_hours_in_df(df)

    # Save the time frame of the data
    start_date = df.index[0]
    end_date = df.index[-1]

    hours_of_day = df.columns
    posts_per_hour = df.sum()

    # Plot the total posts per hour as Bar Graph
    figure_file_name = "total_posts_per_hour"

    plt.figure(figsize=(10, 6))
    plt.bar(hours_of_day, posts_per_hour)
    plt.title(f"Total Posts per Hour ({start_date} - {end_date})")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Total Number of Posts")
    plt.xticks(rotation=45)
    plt.tight_layout()

    if download_data:
        save_graph(figure_file_name=figure_file_name, format=format, post_LLM=post_LLM)
    else:
        plt.show()

    # Plot the average posts per hour for each month as Line Graph
    figure_file_name = "avg_posts_per_hour"

    plt.figure(figsize=(12, 8))

    # plot data for each month in the dataframe
    for time_frame, data in df.iterrows():
        plt.plot(hours_of_day, data, label=time_frame)

    plt.title("Posts per Hour (Different Months in Different Colors)", fontsize=16)
    plt.xlabel("Hour of the Day", fontsize=12)
    plt.ylabel("Posts", fontsize=12)
    plt.xticks(rotation=90)

    plt.legend(title="Month-Year", bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()

    if download_data:
        save_graph(figure_file_name=figure_file_name, format=format, post_LLM=post_LLM)
    else:
        plt.show()


def monthly_data():
    """
    The file processes the following data: Num posts per period, Avg num of posts per day,
    Avg num of replies per posts, Num of new questions posted per period, Post replies,
    Average replies generated daily, Avg View Count Per question, Avg Score per question,
    Avg length of body per question, Account created per period, Number of active users,
    Avg num of daily users, Avg length of body per answer, Avg highest score for a question
    answered to a question with over 500 views.
    """


def popular_tags():
    """
    The file processed contains the 20 most popular tags and the number of
    posts associated with each tag. Any blank data row represents a tag
    that was not present in the top 20 for that month.
    """


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


def save_graph(figure_file_name: str, format: str, post_LLM: bool):
    configured_file = figure_file_name + "." + format
    if post_LLM:
        graph_type = "post_LLM_graphs"
    else:
        graph_type = "pre_LLM_graphs"
    try:
        plt.savefig(f"src/{graph_type}/{configured_file}", format=format)
    except FileNotFoundError:
        os.makedirs(f"src/{graph_type}", exist_ok=True)
        plt.savefig(f"src/{graph_type}/{configured_file}", format=format)
