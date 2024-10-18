import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


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

    def barplot(figure_file_name="total_posts_per_hour_bar_graph"):
        """
        Plot the total posts per hour as Bar Graph
        """

        plt.figure(figsize=(10, 6))
        plt.bar(hours_of_day, posts_per_hour)
        plt.title(f"Total Posts per Hour ({start_date} - {end_date})")
        plt.xlabel("Hour of the Day")
        plt.ylabel("Total Number of Posts")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if download_data:
            save_graph(
                figure_file_name=figure_file_name, format=format, post_LLM=post_LLM
            )
        else:
            plt.show()

    def line_graph(figure_file_name="avg_posts_per_hour_line_graph"):
        plt.figure(figsize=(12, 8))
        """
        Plots the average posts per hour for each month as Line Graph
        """

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
            save_graph(
                figure_file_name=figure_file_name, format=format, post_LLM=post_LLM
            )
        else:
            plt.show()

    barplot()
    line_graph()


def avg_posts_ph_comparison(
    pre_llm_csv_file: str = None,
    post_llm_csv_file: str = None,
    download_data: bool = False,
    format: str = "png",
):
    try:
        pre_llm_df = pd.read_csv(f"CSV_files/{pre_llm_csv_file}")
        post_llm_df = pd.read_csv(f"CSV_files/{post_llm_csv_file}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Please provide a valid CSV file path. Either the file {pre_llm_csv_file} or {post_llm_csv_file} was not found in the CSV_files directory."
        )

    def lineplot(figure_file_name="avg_posts_ph_line_plot"):
        """
        This line plot compares the average number of posts per hour throughout the day for both the pre-LLM and post-LLM periods
        """
        pre_llm_df_converted = convert_hours_in_df(
            pre_llm_df.drop(columns=["Start Date", "End Date"])
        )
        post_llm_df_converted = convert_hours_in_df(
            post_llm_df.drop(columns=["Start Date", "End Date"])
        )

        pre_llm_avg = pre_llm_df_converted.mean(axis=0)
        post_llm_avg = post_llm_df_converted.mean(axis=0)

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

        if download_data:
            save_comparison_graph(figure_file_name=figure_file_name, format=format)
        else:
            plt.show()

    lineplot()


def monthly_data(
    download_data: bool = False,
    format: str = "png",
    csv_file: str = None,
    post_LLM: bool = None,
):
    """
    The file processes the following data: Num posts per period, Avg num of posts per day,
    Avg num of replies per posts, Num of new questions posted per period, Post replies,
    Average replies generated daily, Avg View Count Per question, Avg Score per question,
    Avg length of body per question, Account created per period, Number of active users,
    Avg num of daily users, Avg length of body per answer, Avg highest score for a question
    answered to a question with over 500 views.
    """


def popular_tags(
    download_data: bool = False,
    format: str = "png",
    csv_file: str = None,
    post_LLM: bool = None,
):
    """
    The file processed contains the 20 most popular tags and the number of
    posts associated with each tag. Any blank data represents a tag that
    was not present in the top 20 for that month.
    """

    try:
        df = pd.read_csv(f"CSV_files/{csv_file}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Please provide a valid CSV file path. The file {csv_file} was not found in the CSV_files directory."
        )

    data_long = df.melt(id_vars=["Tag"], var_name="Month", value_name="Count")
    data_long["Month"] = pd.to_datetime(data_long["Month"], format="%b-%y")
    data_long["Count"].fillna(0, inplace=True)

    def popularity_heatmap(figure_file_name="tag_popularity_heatmap"):
        """
        The popularity heatmap visualizes the popularity of the top 20 Stack Overflow tags across the months.
        Darker colors represent higher usage counts, while lighter colors indicate less frequent use
        or absence from the top 20 in a particular month.
        """
        plt.style.use("seaborn-darkgrid")

        plt.figure(figsize=(12, 8))
        pivot_data = df.pivot_table(index="Tag", values=df.columns[1:], aggfunc=np.sum)
        sns.heatmap(pivot_data, cmap="YlGnBu", linewidths=0.5, annot=False)
        plt.title("Tag Popularity Heatmap (Top 20 Tags Over Time)", fontsize=16)
        plt.xlabel("Month")
        plt.ylabel("Tag")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if download_data:
            save_graph(
                figure_file_name=figure_file_name, format=format, post_LLM=post_LLM
            )
        else:
            plt.show()

    def usage_trends_line_graph(figure_file_name="tag_usage_trends_line_graph"):
        """
        Each line represents the count of posts for a particular tag. If the tag count is zero this mean this tag was not used
        enough to be in the top 20 tags for that month.
        """
        plt.figure(figsize=(14, 8))

        sns.lineplot(data=data_long, x="Month", y="Count", hue="Tag", linewidth=2)

        plt.title("Tag Usage Trends Over Time (Top 20 Tags)", fontsize=16)
        plt.xlabel("Month")
        plt.ylabel("Tag Usage Count")
        plt.xticks(rotation=45)
        plt.legend(loc="upper right", bbox_to_anchor=(1.15, 1), ncol=1)

        plt.tight_layout()
        if download_data:
            save_graph(
                figure_file_name=figure_file_name, format=format, post_LLM=post_LLM
            )
        else:
            plt.show()

    def correlation_heatmap(figure_file_name="tag_correlation_heatmap"):
        """
        The correlation heatmap shows how different tags relate to one another in terms of their usage patterns over time.
        Dark red areas indicate strong positive correlations (tags that tend to rise and fall together), while dark blue
        areas indicate negative correlations.
        """
        correlation_matrix = df.set_index("Tag").transpose().corr()

        plt.figure(figsize=(12, 8))
        sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", linewidths=0.5)
        plt.title("Correlation Heatmap of Tag Usage (Top 20 Tags)", fontsize=16)
        plt.xlabel("Tag")
        plt.ylabel("Tag")
        plt.tight_layout()

        if download_data:
            save_graph(
                figure_file_name=figure_file_name, format=format, post_LLM=post_LLM
            )
        else:
            plt.show()

    popularity_heatmap()
    usage_trends_line_graph()
    correlation_heatmap()


def popular_tags_comparison(
    pre_llm_csv_file: str = None,
    post_llm_csv_file: str = None,
    download_data: bool = False,
    format: str = "png",
):
    try:
        pre_llm_df = pd.read_csv(f"CSV_files/{pre_llm_csv_file}")
        post_llm_df = pd.read_csv(f"CSV_files/{post_llm_csv_file}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Please provide a valid CSV file path. Either the file {pre_llm_csv_file} or {post_llm_csv_file} was not found in the CSV_files directory."
        )

    pre_llm_df.columns = [
        f"{col}_preLLM" if col != "Tag" else col for col in pre_llm_df.columns
    ]
    post_llm_df.columns = [
        f"{col}_postLLM" if col != "Tag" else col for col in post_llm_df.columns
    ]

    combined_df = pd.merge(pre_llm_df, post_llm_df, on="Tag", how="outer")

    def barplot(figure_file_name: str = "tag_usage_bar_graph"):
        """
        Display the total usage of each tag in the pre-LLM and post-LLM periods.
        """

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

        if download_data:
            save_comparison_graph(figure_file_name=figure_file_name, format=format)
        else:
            plt.show()

    def scatter_plot(
        descriptive: bool = True, figure_file_name: str = "tag_popularity_scatter_plot"
    ):
        """
        Display how popular each tag is in the pre-LLM and post-LLM periods.Tags are given a popularity rank based on their total usage count.
        """

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
        plt.plot([0, 20], [0, 20], "k--", linewidth=2)  # Diagonal line for reference
        plt.tight_layout()
        if download_data:
            save_comparison_graph(figure_file_name=figure_file_name, format=format)
        else:
            plt.show()

    barplot()
    scatter_plot()


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


def save_comparison_graph(figure_file_name, format):
    configured_file = figure_file_name + "." + format
    try:
        plt.savefig(f"src/comparison_graphs/{configured_file}", format=format)
    except FileNotFoundError:
        os.makedirs(f"src/comparison_graphs", exist_ok=True)
        plt.savefig(f"src/comparison_graphs/{configured_file}", format=format)
