from src.graph_generation import *


def data_processing():
    """
    Calls to functions that read in CSV data from files which contain
    monthly Stack Overflow data from the first to the last of the month
    starting from December 1st 2018 to September 30th 2020
    """
    avg_posts_ph(
        download_data=True,
        format="png",
        csv_file="pre-llm-avg-posts-per-hour.csv",
        post_LLM=False,
    )
    # monthly_data(download_data)
    # popular_tags(download_data)


if __name__ == "__main__":
    data_processing()
