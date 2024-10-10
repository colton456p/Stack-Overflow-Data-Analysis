import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def data_preprocessing():
    """
    Note: per hour = ph
    """
    avg_posts_ph = pd.read_csv("CSV_files/pre-llm-avg-posts-per-hour.csv")

    avg_posts_ph_head = avg_posts_ph.head()

    print(avg_posts_ph_head)


if __name__ == "__main__":
    data_preprocessing()
