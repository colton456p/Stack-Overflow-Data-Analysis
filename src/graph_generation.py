import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from src.data_handling import *


def avg_posts_ph(
    download_data: bool = False,
    format: str = "png",
    csv_file: str = None,
    post_LLM: bool = None,
):
    """
    Processes a CSV file containing the average number of posts per hour.

    Parameters:
        download_data (bool): Whether to download the generated data.
        file_format (str): Format to save the graph (e.g., 'png').
        csv_file (str): Path to the CSV file containing the data.
        post_llm (bool): Flag indicating if the data is from post-LLM periods.
    """
    if post_LLM is None:
        raise ValueError("Please provide a value for the post_LLM parameter.")

    try:
        df = pd.read_csv(f"CSV_files/{csv_file}", index_col=0)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"CSV file '{csv_file}' not found. Ensure the file is located in the 'CSV_files' directory."
        ) from e

    df = df.drop(df.columns[0], axis=1)
    df = np.floor(df).astype(int)
    df = convert_hours_in_df(df)

    start_date = df.index[0]
    end_date = df.index[-1]

    hours_of_day = df.columns
    posts_per_hour = df.sum()

    def barplot(figure_file_name="total_posts_per_hour_bar_graph"):
        """Total posts per hour as Bar Graph"""
        plt.figure(figsize=(10, 6))
        plt.bar(hours_of_day, posts_per_hour)
        plt.title(f"Total Posts per Hour ({start_date} - {end_date})")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Total Number of Posts")
        plt.xticks(rotation=45)
        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    def line_graph(figure_file_name="avg_posts_per_hour_line_graph"):
        """Generates a line graph comparing posts per hour for different time periods."""
        mid_point = len(df) // 2
        df_part1, df_part2 = df.iloc[:mid_point], df.iloc[mid_point:]

        fig, axes = plt.subplots(2, 1, figsize=(12, 16))

        for time_frame, data in df_part1.iterrows():
            axes[0].plot(hours_of_day, data, label=time_frame)
        axes[0].set_title("Posts per Hour (First 11 Months)", fontsize=16)
        axes[0].set_xlabel("Hour of the Day", fontsize=12)
        axes[0].set_ylabel("Posts", fontsize=12)
        axes[0].legend(title="Month-Year", bbox_to_anchor=(1.05, 1), loc="upper left")
        axes[0].tick_params(axis="x", rotation=90)

        for time_frame, data in df_part2.iterrows():
            axes[1].plot(hours_of_day, data, label=time_frame)
        axes[1].set_title("Posts per Hour (Next 11 Months)", fontsize=16)
        axes[1].set_xlabel("Hour of the Day", fontsize=12)
        axes[1].set_ylabel("Posts", fontsize=12)
        axes[1].legend(title="Month-Year", bbox_to_anchor=(1.05, 1), loc="upper left")
        axes[1].tick_params(axis="x", rotation=90)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    barplot()
    line_graph()


def avg_posts_ph_comparison(
    pre_llm_csv_file: str = None,
    post_llm_csv_file: str = None,
    download_data: bool = False,
    format: str = "png",
):
    """
    Compares the average posts per hour between pre-LLM and post-LLM periods.

    Parameters:
        pre_llm_csv_file (str): Path to the pre-LLM data CSV.
        post_llm_csv_file (str): Path to the post-LLM data CSV.
        download_data (bool): Whether to download the generated graph.
        file_format (str): Format to save the graph (e.g., 'png').
    """
    try:
        pre_llm_df = pd.read_csv(f"CSV_files/{pre_llm_csv_file}")
        post_llm_df = pd.read_csv(f"CSV_files/{post_llm_csv_file}")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"One or both of the CSV files ('{pre_llm_csv_file}', '{post_llm_csv_file}') were not found."
        ) from e

    def lineplot(figure_file_name="avg_posts_ph_line_plot"):
        """Generates a line plot comparing pre-LLM and post-LLM periods."""
        pre_llm_avg = convert_hours_in_df(
            pre_llm_df.drop(columns=["Start Date", "End Date"])
        ).mean(axis=0)
        post_llm_avg = convert_hours_in_df(
            post_llm_df.drop(columns=["Start Date", "End Date"])
        ).mean(axis=0)

        hourly_posts = pd.DataFrame(
            {
                "Hour": pre_llm_avg.index,
                "Pre-LLM": pre_llm_avg.values,
                "Post-LLM": post_llm_avg.values,
            }
        )

        plt.figure(figsize=(14, 8))
        sns.lineplot(
            x="Hour", y="Pre-LLM", data=hourly_posts, marker="o", label="Pre-LLM"
        )
        sns.lineplot(
            x="Hour", y="Post-LLM", data=hourly_posts, marker="o", label="Post-LLM"
        )

        plt.title("Average Posts Per Hour: Pre-LLM vs. Post-LLM", fontsize=16)
        plt.xlabel("Hour of Day")
        plt.ylabel("Average Posts")
        plt.xticks(rotation=45)
        plt.legend(title="Time Period")
        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    lineplot()


def popular_tags(
    download_data: bool = False,
    format: str = "png",
    csv_file: str = None,
    post_LLM: bool = None,
):
    """
    Processes a CSV file containing the 20 most popular tags and the number of posts associated with each tag per period.
    Any blank data represents a tag that was not present in the top 20 for that month.

    Parameters:
        download_data (bool): Whether to download the generated data.
        file_format (str): Format to save the graph (e.g., 'png').
        csv_file (str): Path to the CSV file containing the data.
        post_llm (bool): Flag indicating if the data is from post-LLM periods.
    """

    try:
        df = pd.read_csv(f"CSV_files/{csv_file}")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"CSV file '{csv_file}' not found. Ensure the file is located in the 'CSV_files' directory."
        ) from e

    data_long = df.melt(id_vars=["Tag"], var_name="Month", value_name="Count")
    data_long["Month"] = pd.to_datetime(data_long["Month"], format="%b-%y")
    data_long["Count"] = data_long["Count"].fillna(0)

    def usage_trends_line_graph(
        figure_file_name="tag_usage_trends_line_graph",
    ):
        """Generates a line graph with 2 subplots where each line represents the count of posts for a particular tag."""
        unique_tags = data_long["Tag"].unique()
        mid_point = len(unique_tags) // 2
        tags_part1 = unique_tags[:mid_point]
        tags_part2 = unique_tags[mid_point:]

        fig, axes = plt.subplots(2, 1, figsize=(14, 16))
        sns.lineplot(
            data=data_long[data_long["Tag"].isin(tags_part1)],
            x="Month",
            y="Count",
            hue="Tag",
            ax=axes[0],
            linewidth=2,
        )

        axes[0].set_title("Tag Usage Trends (First 12 Tags)", fontsize=16)
        axes[0].set_xlabel("Month", fontsize=12)
        axes[0].set_ylabel("Tag Usage Count", fontsize=12)
        axes[0].tick_params(axis="x", rotation=45)
        axes[0].legend(loc="upper right", bbox_to_anchor=(1.15, 1), ncol=1)

        sns.lineplot(
            data=data_long[data_long["Tag"].isin(tags_part2)],
            x="Month",
            y="Count",
            hue="Tag",
            ax=axes[1],
            linewidth=2,
        )

        axes[1].set_title("Tag Usage Trends (Next 12 Tags)", fontsize=16)
        axes[1].set_xlabel("Month", fontsize=12)
        axes[1].set_ylabel("Tag Usage Count", fontsize=12)
        axes[1].tick_params(axis="x", rotation=45)
        axes[1].legend(loc="upper right", bbox_to_anchor=(1.15, 1), ncol=1)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    usage_trends_line_graph()


def popular_tags_comparison(
    pre_llm_csv_file: str = None,
    post_llm_csv_file: str = None,
    download_data: bool = False,
    format: str = "png",
):
    """
    Compares the the 20 most popular tags and the number of posts associated with each tag per period between pre-LLM and post-LLM periods.

    Parameters:
        pre_llm_csv_file (str): Path to the pre-LLM data CSV.
        post_llm_csv_file (str): Path to the post-LLM data CSV.
        download_data (bool): Whether to download the generated graph.
        file_format (str): Format to save the graph (e.g., 'png').
    """
    try:
        pre_llm_df = pd.read_csv(f"CSV_files/{pre_llm_csv_file}")
        post_llm_df = pd.read_csv(f"CSV_files/{post_llm_csv_file}")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"One or both of the CSV files ('{pre_llm_csv_file}', '{post_llm_csv_file}') were not found."
        ) from e

    pre_llm_df.columns = [
        f"{col}_preLLM" if col != "Tag" else col for col in pre_llm_df.columns
    ]
    post_llm_df.columns = [
        f"{col}_postLLM" if col != "Tag" else col for col in post_llm_df.columns
    ]

    combined_df = pd.merge(pre_llm_df, post_llm_df, on="Tag", how="outer")

    def barplot(figure_file_name: str = "tag_usage_bar_graph"):
        """Generates a barplot of the total usage of each tag pre-LLM and post-LLM."""
        combined_df["Total_preLLM"] = combined_df.filter(like="_preLLM").sum(axis=1)
        combined_df["Total_postLLM"] = combined_df.filter(like="_postLLM").sum(axis=1)

        total_usage = combined_df[["Tag", "Total_preLLM", "Total_postLLM"]].set_index(
            "Tag"
        )
        total_usage_melt = total_usage.reset_index().melt(
            id_vars=["Tag"], var_name="Time Period", value_name="Total Count"
        )

        plt.figure(figsize=(14, 8))
        sns.barplot(data=total_usage_melt, x="Tag", y="Total Count", hue="Time Period")
        plt.title("Total Usage of Tags: Pre-LLM vs. Post-LLM", fontsize=16)
        plt.xlabel("Tag")
        plt.ylabel("Total Count")
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    def scatter_plot(
        descriptive: bool = True, figure_file_name: str = "tag_popularity_scatter_plot"
    ):
        """Generates a scatter plot on tag popularity pre-LLM and post-LLM. Tags are given a popularity rank based on their total usage count.
        The higher the score the less popular the tag is."""

        pre_llm_df["Total_preLLM"] = pre_llm_df.filter(like="_preLLM").sum(axis=1)
        post_llm_df["Total_postLLM"] = post_llm_df.filter(like="_postLLM").sum(axis=1)

        pre_llm_df["Rank_preLLM"] = pre_llm_df["Total_preLLM"].rank(ascending=False)
        post_llm_df["Rank_postLLM"] = post_llm_df["Total_postLLM"].rank(ascending=False)

        rank_comparison = pd.merge(
            pre_llm_df[["Tag", "Rank_preLLM"]],
            post_llm_df[["Tag", "Rank_postLLM"]],
            on="Tag",
        )

        plt.figure(figsize=(14, 8))
        scatter = sns.scatterplot(
            data=rank_comparison, x="Rank_preLLM", y="Rank_postLLM", hue="Tag", s=100
        )

        if descriptive:
            for i in range(rank_comparison.shape[0]):
                plt.text(
                    rank_comparison["Rank_preLLM"][i] + 0.1,
                    rank_comparison["Rank_postLLM"][i] + 0.1,
                    rank_comparison["Tag"][i],
                    horizontalalignment="left",
                    size="medium",
                    color="black",
                    weight="semibold",
                )
            figure_file_name += "_descriptive"

        plt.title("Tag Popularity Shift: Pre-LLM vs. Post-LLM", fontsize=16)
        plt.xlabel("Pre-LLM Rank")
        plt.ylabel("Post-LLM Rank")
        plt.plot(
            [0, 20], [0, 20], "k--", linewidth=2
        )  # This diagonal line is just for reference

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    def dual_scatter_plot(
        descriptive: bool = True,
        figure_file_name: str = "tag_popularity_scatter_subplot",
    ):
        """Generates a scatter plot split into two subplots on tag popularity pre-LLM and post-LLM. Tags are given a popularity rank based on their total usage count
        The higher the score the less popular the tag is."""
        pre_llm_df["Total_preLLM"] = pre_llm_df.filter(like="_preLLM").sum(axis=1)
        post_llm_df["Total_postLLM"] = post_llm_df.filter(like="_postLLM").sum(axis=1)

        pre_llm_df["Rank_preLLM"] = pre_llm_df["Total_preLLM"].rank(ascending=False)
        post_llm_df["Rank_postLLM"] = post_llm_df["Total_postLLM"].rank(ascending=False)

        rank_comparison = pd.merge(
            pre_llm_df[["Tag", "Rank_preLLM"]],
            post_llm_df[["Tag", "Rank_postLLM"]],
            on="Tag",
        )

        tags = rank_comparison["Tag"].unique()
        mid_point = len(tags) // 2
        tags_part1 = tags[:mid_point]
        tags_part2 = tags[mid_point:]

        fig, axes = plt.subplots(2, 1, figsize=(14, 16))
        sns.scatterplot(
            data=rank_comparison[rank_comparison["Tag"].isin(tags_part1)],
            x="Rank_preLLM",
            y="Rank_postLLM",
            hue="Tag",
            ax=axes[0],
            s=100,
        )

        if descriptive:
            for i in range(
                len(rank_comparison[rank_comparison["Tag"].isin(tags_part1)])
            ):
                tag_data = rank_comparison[
                    rank_comparison["Tag"].isin(tags_part1)
                ].iloc[i]
                axes[0].text(
                    tag_data["Rank_preLLM"] + 0.1,
                    tag_data["Rank_postLLM"] + 0.1,
                    tag_data["Tag"],
                    horizontalalignment="left",
                    size="medium",
                    color="black",
                    weight="semibold",
                )

        axes[0].set_title("Tag Popularity Shift (First 12 Tags)", fontsize=16)
        axes[0].set_xlabel("Pre-LLM Rank")
        axes[0].set_ylabel("Post-LLM Rank")
        axes[0].plot(
            [0, 20], [0, 20], "k--", linewidth=2
        )  # This diagonal line is just for reference

        sns.scatterplot(
            data=rank_comparison[rank_comparison["Tag"].isin(tags_part2)],
            x="Rank_preLLM",
            y="Rank_postLLM",
            hue="Tag",
            ax=axes[1],
            s=100,
        )

        if descriptive:
            for i in range(
                len(rank_comparison[rank_comparison["Tag"].isin(tags_part2)])
            ):
                tag_data = rank_comparison[
                    rank_comparison["Tag"].isin(tags_part2)
                ].iloc[i]
                axes[1].text(
                    tag_data["Rank_preLLM"] + 0.1,
                    tag_data["Rank_postLLM"] + 0.1,
                    tag_data["Tag"],
                    horizontalalignment="left",
                    size="medium",
                    color="black",
                    weight="semibold",
                )

        axes[1].set_title("Tag Popularity Shift (Next 12 Tags)", fontsize=16)
        axes[1].set_xlabel("Pre-LLM Rank")
        axes[1].set_ylabel("Post-LLM Rank")
        axes[1].plot(
            [0, 20], [0, 20], "k--", linewidth=2
        )  # This diagonal line is just for reference

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    barplot()
    scatter_plot()
    dual_scatter_plot()


def monthly_data(
    download_data: bool = False,
    format: str = "png",
    csv_file: str = None,
    post_LLM: bool = None,
):
    """
    Processes a CSV with the following data: Num posts per period, Avg num of posts per day,
    Avg num of replies per posts, Num of new questions posted per period, Post replies,
    Average replies generated daily, Avg View Count Per question, Avg Score per question,
    Avg length of body per question, Account created per period, Number of active users,
    Avg num of daily users, Avg length of body per answer, Avg highest score for a question
    answered to a question with over 500 views.

    Parameters:
        download_data (bool): Whether to download the generated data.
        file_format (str): Format to save the graph (e.g., 'png').
        csv_file (str): Path to the CSV file containing the data.
        post_llm (bool): Flag indicating if the data is from post-LLM periods.
    """
    try:
        df = pd.read_csv(f"CSV_files/{csv_file}", index_col=False)
    except FileNotFoundError as e:
        raise FileNotFoundError(
            f"CSV file '{csv_file}' not found. Ensure the file is located in the 'CSV_files' directory."
        ) from e

    df = df.reset_index(drop=True)
    df["Start Date"] = pd.to_datetime(df["Start Date"], format="%b-%y")

    def post_engagement_line_graph(figure_file_name="post_engagement_line_graph"):
        """Generates a line graph which shows the change in post engagement (Num posts per period + Avg num of posts per day)"""
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(
            df["Start Date"],
            df["Num posts per period"],
            label="Num posts per period",
            marker="o",
        )
        plt.xlabel("Month")
        plt.ylabel("Number of Posts")
        plt.title("Number of Posts per Period")
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.subplot(1, 2, 2)
        plt.plot(
            df["Start Date"],
            df["Avg num of posts per day"],
            label="Avg num of posts per day",
            marker="o",
            color="purple",
        )
        plt.xlabel("Month")
        plt.ylabel("Average Number of Posts Per Day")
        plt.title("Average Posts Per Day")
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    def post_replies_line_graph(figure_file_name="post_replies_line_graph"):
        """Generates a line graph to show the number of post replies (Num of post replies + Avg number of replies per day)"""
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.plot(
            df["Start Date"],
            df["Post replies"],
            label="Post replies",
            marker="o",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Number of Replies")
        plt.title("Post Replies per Period")
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.subplot(1, 2, 2)
        plt.plot(
            df["Start Date"],
            df["Average replies generated daily"],
            label="Avg replies per day",
            marker="o",
            color="green",
        )
        plt.xlabel("Month")
        plt.ylabel("Average Replies Per Day")
        plt.title("Average Replies Per Day")
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    def avg_view_per_post_line_graph(figure_file_name="avg_view_per_post_line_graph"):
        """Generates a line graph to show the average view count per post"""
        plt.figure(figsize=(10, 6))
        plt.plot(
            df["Start Date"],
            df["Avg View Count Per question"],
            label="Avg View Count Per question",
            marker="o",
            color="purple",
        )
        plt.xlabel("Month")
        plt.ylabel("Average View Count")
        plt.title("Average View Count Per Post")
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    def length_body_line_graph(figure_file_name="length_body_line_graph"):
        """Generates a line graph to compare the average length of body per question and per answer"""
        plt.figure(figsize=(10, 6))
        plt.plot(
            df["Start Date"],
            df["Avg length of body per question"],
            label="Avg length of body per question",
            marker="o",
            color="red",
        )
        plt.plot(
            df["Start Date"],
            df["Avg length of body per answer"],
            label="Avg length of body per answer",
            marker="o",
            color="blue",
        )
        plt.xlabel("Month")
        plt.ylabel("Average Length (characters)")
        plt.title("Average Length of Body Per Question vs Answer")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    def user_activity_bar_graph(figure_file_name="user_activity_bar_graph"):
        """Generates a bar chart comparing accounts created per period, active users, and avg daily users"""
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        bar_width = 0.35
        index = np.arange(len(df["Start Date"]))

        plt.bar(
            index,
            df["Account created per period"],
            bar_width,
            label="Account created per period",
            color="skyblue",
        )
        plt.bar(
            index + bar_width,
            df["Number of active users"],
            bar_width,
            label="Number of active users",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Count")
        plt.title("Accounts Created vs Active Users")
        plt.xticks(
            index + bar_width / 2,
            [d.strftime("%b-%y") for d in df["Start Date"]],
            rotation=45,
        )
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.bar(
            index,
            df["Avg num of daily users"],
            bar_width,
            label="Avg daily users",
            color="green",
        )
        plt.xlabel("Month")
        plt.ylabel("Avg Daily Users")
        plt.title("Average Daily Users")
        plt.xticks(index, [d.strftime("%b-%y") for d in df["Start Date"]], rotation=45)

        plt.tight_layout()
        create_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
            post_LLM=post_LLM,
        )

    post_engagement_line_graph()
    post_replies_line_graph()
    avg_view_per_post_line_graph()
    length_body_line_graph()
    user_activity_bar_graph()


def monthly_data_comparison(
    pre_llm_csv_file: str = None,
    post_llm_csv_file: str = None,
    download_data: bool = False,
    format: str = "png",
):
    """
    Processes a pre LLM and post LLM CSV with the following data: Num posts per period, Avg num of posts per day,
    Avg num of replies per posts, Num of new questions posted per period, Post replies,
    Average replies generated daily, Avg View Count Per question, Avg Score per question,
    Avg length of body per question, Account created per period, Number of active users,
    Avg num of daily users, Avg length of body per answer, Avg highest score for a question
    answered to a question with over 500 views.

    Parameters:
        pre_llm_csv_file (str): Path to the pre-LLM data CSV.
        post_llm_csv_file (str): Path to the post-LLM data CSV.
        download_data (bool): Whether to download the generated graph.
        file_format (str): Format to save the graph (e.g., 'png').
    """
    pre_llm_data = pd.read_csv(f"CSV_files/{pre_llm_csv_file}")
    post_llm_data = pd.read_csv(f"CSV_files/{post_llm_csv_file}")
    pre_llm_data["Start Date"] = pd.to_datetime(
        pre_llm_data["Start Date"], format="%b-%y"
    )
    post_llm_data["Start Date"] = pd.to_datetime(
        post_llm_data["Start Date"], format="%b-%y"
    )

    def num_questions_line_graph(figure_file_name="num_questions_line_graph"):
        """Generates line graph to compare the number of questions asked per period Pre LLM vs Post LLM"""
        plt.figure(figsize=(10, 6))
        plt.plot(
            pre_llm_data["Start Date"],
            pre_llm_data["Num of new questions posted per period"],
            label="Pre LLM",
            marker="o",
            color="blue",
        )
        plt.plot(
            post_llm_data["Start Date"],
            post_llm_data["Num of new questions posted per period"],
            label="Post LLM",
            marker="o",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Number of Questions")
        plt.title("Number of Questions Asked Per Period (Pre LLM vs Post LLM)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    def body_length_answer_line_graph(
        figure_file_name="length_of_body_answer_line_graph",
    ):
        """Generates a line graph comparing avg length of body per answer pre LLM vs post LLM"""
        plt.figure(figsize=(10, 6))
        plt.plot(
            pre_llm_data["Start Date"],
            pre_llm_data["Avg length of body per answer"],
            label="Pre LLM",
            marker="o",
            color="blue",
        )
        plt.plot(
            post_llm_data["Start Date"],
            post_llm_data["Avg length of body per answer"],
            label="Post LLM",
            marker="o",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Avg Length of Body (Answer)")
        plt.title("Avg Length of Body per Answer (Pre LLM vs Post LLM)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    def body_length_question_line_graph(
        figure_file_name="length_of_body_question_line_graph",
    ):
        """Generates a line graph comparing avg length of body per question pre LLM vs post LLM"""
        plt.figure(figsize=(10, 6))
        plt.plot(
            pre_llm_data["Start Date"],
            pre_llm_data["Avg length of body per question"],
            label="Pre LLM",
            marker="o",
            color="blue",
        )
        plt.plot(
            post_llm_data["Start Date"],
            post_llm_data["Avg length of body per question"],
            label="Post LLM",
            marker="o",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Avg Length of Body (Question)")
        plt.title("Avg Length of Body per Question (Pre LLM vs Post LLM)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    def post_per_period_line_graph(figure_file_name="post_per_period_line_graph"):
        """Generates a line graph comparing number of posts per period pre LLM vs post LLM"""
        plt.figure(figsize=(10, 6))
        plt.plot(
            pre_llm_data["Start Date"],
            pre_llm_data["Num posts per period"],
            label="Pre LLM",
            marker="o",
            color="blue",
        )
        plt.plot(
            post_llm_data["Start Date"],
            post_llm_data["Num posts per period"],
            label="Post LLM",
            marker="o",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Number of Posts")
        plt.title("Number of Posts Per Period (Pre LLM vs Post LLM)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    def view_count_scatter_plot(figure_file_name="view_count_scatter_plot"):
        """Generates a line graph comparing avg view count per question pre LLM vs post LLM"""
        plt.figure(figsize=(10, 6))
        plt.scatter(
            pre_llm_data["Start Date"],
            pre_llm_data["Avg View Count Per question"],
            label="Pre LLM",
            color="blue",
        )
        plt.scatter(
            post_llm_data["Start Date"],
            post_llm_data["Avg View Count Per question"],
            label="Post LLM",
            color="orange",
        )
        plt.xlabel("Month")
        plt.ylabel("Avg View Count Per Question")
        plt.title("Avg View Count Per Question (Pre LLM vs Post LLM)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)

        plt.tight_layout()
        create_comparison_graph(
            download_data=download_data,
            figure_file_name=figure_file_name,
            format=format,
        )

    num_questions_line_graph()
    body_length_answer_line_graph()
    body_length_question_line_graph()
    post_per_period_line_graph()
    view_count_scatter_plot()
