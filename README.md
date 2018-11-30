# Florida Man Game

Welcome to the Florida Man game! This is a pretty simple game using Markov
Chains to generate real and fake "Florida Man" headlines. Your goal is to
distinguish between the real headlines, and the fake headlines!

## How To Play

```shell
cd src
python main.py
```

## Data Source

The datasource for the Markov Chains was a giant Reddit datadump on Google
BigQuery. The exact query I used can be found in the `query.sql` file.

Since the dataset's pretty small, the data can be found in
`src/data/real_reddit_posts.csv`.