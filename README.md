# PoliTopics
Deriving Political Party Affiliation With Diffusion Maps
Paper: https://healyt22.github.io/papers/Healy_Timothy_DiffusionMaps_Project.pdf

The idea of this project is to use nonlinear dimensionality reduction to uncover semantic relationships between articles of text data. In this application a [Diffusion Map](https://arxiv.org/pdf/math/0503445.pdf) is applied to US Politican tweets, uncovering a "political spectrum" underpinning their rhetoric on Twitter.

Here are the main components being utilized by `politopics/politopics.py`
1. Getting tweet data from the Twitter API
    `politopics/util/twitter_api.py`
2. Parsing & Cleaning Tweets
    `politopics/util/tweet_interface.py`
3. Loading tweets into local MySQL database
    `politopics/util/mysql_interface.py`
4. Generating Diffusion Map
    `politopics/analysis/diffusion_map.py`
5. Visualizing the Political spectrum
    `politopics/analysis/visualize.py`

Proof of concept can be seen in `Diffusion Map.ipynb`
