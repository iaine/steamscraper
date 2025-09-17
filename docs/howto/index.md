## HowTo

```python
from steam import SteamScraper
scraper = SteamScraper()
```

### Search

```python

term = "banana"
ls = scraper.get_search(term)
scraper.write_csv(scraper.get_links_details(ls), f"{term}_steam_search.csv") 
```

### Search by Publisher

```python
term = "Sky"
ls = scraper.get_publisher(term)
scraper.write_csv(scraper.get_links_details(ls), f"{term}_steam_publisher.csv")
```

### Search by Developer

```python
term = "Sky"
ls = scraper.get_developer(term)
scraper.write_csv(scraper.get_links_details(ls), f"{term}_steam_publisher.csv")
```
### Search by Similar

```python
term = 2923300
ls = scraper.get_similar(term)
scraper.write_csv(scraper.get_links_details(ls), f"{term}_steam_similar.csv")
```