# PoliTopics
Deriving Political Party Affiliation With Diffusion Maps

Paper: https://healyt22.github.io/papers/Healy_Timothy_DiffusionMaps_Project.pdf

The idea of this project is to use nonlinear dimensionality reduction to uncover semantic relationships between articles of text data. In this application a [Diffusion Map](https://arxiv.org/pdf/math/0503445.pdf) is applied to US Politican tweets, uncovering a "political spectrum" underpinning their rhetoric on Twitter.

Here are the main components being utilized by `politopics/politopics.py`
1. `politopics/twitter_api.py` gets tweet data from the Twitter API    
2. `politopics/tweet_interface.py` parses & cleans tweets
3. `politopics/mysql_interface.py` loads tweets into local MySQL database
4. `politopics/diffusion_map.py` generates Diffusion Map
5. `politopics/visualize.py` visualizes the political spectrum

Proof of concept can be seen in `Diffusion Map.ipynb`

This library is run via Airflow on a GPU-equipped local machine I built.
