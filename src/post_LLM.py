from src.graph_generation import *


def data_processing():
    """
    Calls to functions that read in CSV data from files which contain
    monthly Stack Overflow data from the first to the last of the month
    starting from December 1st 2022 to September 30th 2024
    """
    avg_posts_ph(
        download_data=True,
        csv_file="post-llm-avg-posts-per-hour.csv",
        post_LLM=True,
    )
    monthly_data(
        download_data=True,
        csv_file="post-llm-monthly-data.csv",
        post_LLM=True,
    )
    popular_tags(
        download_data=True,
        csv_file="post-llm-popular-tags.csv",
        post_LLM=True,
    )


if __name__ == "__main__":
    data_processing()
