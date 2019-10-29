# DataRetrival

# Plan

1. Crawl Data (around 50)
2. Convert words to embeddings (bag of vectors)
3. K means
4. profit !!!


# How to run files

To crawl and scrape:
```
python3 manage.py scrap --num_pages {number pages to scrap} --timeout {time between calls}
```

To query:
```
python3 manage.py scrap --query "{query}"
```
