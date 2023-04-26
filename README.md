# Twitter Scraper

A Python script for scraping tweets from Twitter profiles using Selenium and BeautifulSoup. This script can be used to extract the tweets of any public Twitter account. 

## Installation

1. Clone this repository to your local machine.

```bash
git clone https://github.com/your_username/selenium-twitter-scraper.git
```

2. Install the required packages.

## Usage

The `getUserTweets()` function in `tscraper.py` is used to extract tweets from a specified Twitter profile. This function takes the following arguments:

- `user`: The Twitter handle of the profile you wish to scrape.
- `count`: The maximum number of tweets to scrape. Defaults to 10.
- `retweeted`: Whether to include retweets in the scraped data. Defaults to `False`.
- `image`: Whether to include tweets with images in the scraped data. Defaults to `False`.
- `video`: Whether to include tweets with videos in the scraped data. Defaults to `False`.

```python

from tscraper import getUserTweets

tweets = getUserTweets("elonmusk", count=20, retweeted=True, image=True, video=True)

for tweet in tweets:
    print(tweet)
```

## Notes

- This script uses Selenium to automate the process of scrolling through the Twitter profile and loading additional tweets. As a result, it may take some time to scrape a large number of tweets.

## Contact

```python
from discord import YmirSG#5599
from instagram import sonmez.md
```
