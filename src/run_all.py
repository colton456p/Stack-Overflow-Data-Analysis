from src.comparison_LLM import data_processing as comparison_llm_data_processing
from src.post_LLM import data_processing as post_llm_data_processing
from src.pre_LLM import data_processing as pre_llm_data_processing


def main():
    """
    Runs all graph generation scripts simultaneously
    """
    post_llm_data_processing()
    pre_llm_data_processing()
    comparison_llm_data_processing()


if __name__ == "__main__":
    main()
