from src.graph_generation import create_graphs


def main():
    """
    Calls to functions that read in CSV data from files which contain
    monthly Stack Overflow data from the first to the last of the month
    starting from December 1st 2022 to September 30th 2024
    """
    create_graphs(
        download_data=True,
        format="png",
        csv_file="post-llm-avg-posts-per-hour.csv",
        post_LLM=True,
    )


if __name__ == "__main__":
    main()
