# Research Study: Stack Overflow Usage Pre vs Post LLM
- **Pre LLM time period:** December 1st 2018 - September 30th 2020
- **Post LLM time period:** December 1st 2022 - September 30th 2024

## Data research plan:
#### Posts:
- [X] Average number of posts
- [X] Average number of posts per day
- [X] Average length of body of post
- [ ] Average number of posts per hour of the day
#### Questions:
- [X] Number of questions posted
- [X] Average score per question
- [X] Average view count per question
#### Answers:
- [X] Average number of reply's per post
- [X] Number of post reply's
- [X] The average of the number of reply's per day
- [X] Average length of answer
- [X] Average number of votes per top answer
#### Users:
- [X] Average number of accounts created
- [X] Number of active users
- [X] Average number of dailey users
#### Quality of responses:
- [ ] Record the quality of responses using an error checking software such as FindBug
- [ ] Record whether or not the quality/length/description in answers on Stack Overflow have improved or disimproved.
#### Popularity of topics discussed
- [X] Determine which topics/coding languages are most searched/tagged in posts.
- [X] Count the number of tags accosiated to each topic.


# Installation guide:
1. Create virtual environment:
    ```bash
    python3 -m venv venv
    ```
2. Install Pandas, Numpy, and Matplotlib
    ```bash
    pip install pandas numpy matplotlib
    ```
3. Run the Pre vs Post LLM graph generation seperately
    - Pre LLM:
        ```bash
        python3 -m src.pre_llm_graph_generation
        ```
    - Post LLM:
        ```bash
        python3 -m src.post_llm_graph_generation
        ```