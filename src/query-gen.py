import datetime

FORMAT_STR = "SELECT title, url, score FROM `fh-bigquery.reddit_posts.{}_{}`"

SUBREDDIT = "FloridaMan"
WHERE_CLAUSE = f" WHERE subreddit = '{SUBREDDIT}' AND score >= 5"

JOIN_STR = " UNION DISTINCT "

queries = [
    "SELECT title, url, score FROM `fh-bigquery.reddit_posts.full_corpus_201512`"
    + WHERE_CLAUSE
]
for year in range(2016, 2019):
    for month in range(1, 13):
        month_str = str(month) if month > 9 else "0" + str(month)
        queries.append(FORMAT_STR.format(year, month_str) + WHERE_CLAUSE)

remaining_months = 13 - datetime.date.today().month
queries = queries[:-remaining_months]

with open("query.sql", "w+") as f:
    f.write(JOIN_STR.join(queries) + " ORDER BY score DESC")
