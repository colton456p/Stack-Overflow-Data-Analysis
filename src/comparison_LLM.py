from src.graph_generation import *


def data_processing():
    """
    Calls to functions that read in CSV data from files which contain
    monthly Stack Overflow data from the first to the last of the month
    starting from December 1st 2022 to September 30th 2024
    """
    popular_tags_comparison(
        pre_llm_csv_file="pre-llm-popular-tags.csv",
        post_llm_csv_file="post-llm-popular-tags.csv",
        download_data=True,
    )

    avg_posts_ph_comparison(
        pre_llm_csv_file="pre-llm-avg-posts-per-hour.csv",
        post_llm_csv_file="post-llm-avg-posts-per-hour.csv",
        download_data=True,
    )


if __name__ == "__main__":
    data_processing()
