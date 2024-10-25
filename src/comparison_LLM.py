from src.graph_generation import *


def data_processing():
    """
    Calls to functions that read in both the pre LLM CSV data and post LLM CSV data from files
    which contain monthly Stack Overflow data from the first to the last of the month for the
    given period.
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
    monthly_data_comparison(
        pre_llm_csv_file="pre-llm-monthly-data.csv",
        post_llm_csv_file="post-llm-monthly-data.csv",
        download_data=True,
    )


if __name__ == "__main__":
    data_processing()
