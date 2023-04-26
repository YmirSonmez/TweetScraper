from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager


class Tweet:
    isRetweeted: bool
    isVideo: bool
    isImage: bool

    author: str
    date: str
    content: str

    def getTimeMillis(self):
        date = datetime.fromisoformat(self.date.replace("Z", "+00:00"))
        return int(date.timestamp() * 1000)

    def getKey(self):
        return str(self.getTimeMillis()) + self.author

    def __str__(self):
        return f"Author: {self.author}\nDate: {self.date}\nContent: {self.content}\nIs Retweeted: {self.isRetweeted}\nIs Video: {self.isVideo}\nIs Image: {self.isImage}"

    @staticmethod
    def fromHtml(html):
        soup = BeautifulSoup(html, "lxml")

        # print(soup)
        tweet = Tweet()
        tweet.isVideo = Tweet.findVideo(soup)
        tweet.isImage = Tweet.findImage(soup)
        tweet.isRetweeted = Tweet.findRetweeted(soup)
        # print(html)
        author = soup.find('span', class_="css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0")
        if author:
            tweet.author = author.text
            val = soup.find('div', attrs={"data-testid": "tweetText"})
            tweet.content = val.text if val else ""
            tweet.date = soup.find("time").get("datetime")
        else:
            return None

        # print(tweet.author)
        # print(tweet.isVideo)
        # print(tweet.isImage)
        # print(tweet.isRetweeted)
        # print(tweet.content)
        # print(tweet.date)
        # print(tweet.getTimeMillis())
        return tweet

    @staticmethod
    def exists(dict, html):
        key = Tweet.generateKey(html)
        if key:
            return key in dict
        else:
            return True

    @staticmethod
    def generateKey(html):
        author = html.find('span', class_="css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0")
        if author:
            return html.find("time").get("datetime") + author.text
        else:
            return None

    @staticmethod
    def findRetweeted(soup):
        return bool(soup.find('span',
                              class_="css-901oao css-16my406 css-cens5h r-1bwzh9t r-poiln3 r-n6v787 r-b88u0q r-1cwl3u0 r-bcqeeo r-qvutc0"))

    @staticmethod
    def findImage(soup):
        return len(soup.findAll('img')) > 1

    @staticmethod
    def findVideo(soup):
        return bool(soup.find('video'))


def getUserTweets(user, count=10, retweeted=False, image=False, video=False):
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--silent')
    chrome_options.add_argument('--disable-logging')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://twitter.com/{0}".format(user))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,
                                                                      "/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/section/div/div/div[1]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div/div/div/div/div")))
    d = {}

    x = 1

    tweetCount = int(
        "".join(
            filter(str.isdigit, BeautifulSoup(driver.page_source, "lxml").find("div",
                                                                               class_="css-901oao css-1hf3ou5 r-1bwzh9t r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-bcqeeo r-qvutc0").text)))

    count = tweetCount if tweetCount < count else count

    while True:
        page = BeautifulSoup(driver.page_source, "lxml")
        tweets = page.find('section', class_="css-1dbjc4n").findAll('div', attrs={
            "data-testid": "cellInnerDiv"})

        for t in tweets:
            isVideo = Tweet.findVideo(t)
            isImage = Tweet.findImage(t)
            isRetweeted = Tweet.findRetweeted(t)

            if not Tweet.exists(d, t):
                if retweeted or not isRetweeted:
                    if image or not isImage:
                        if video or not isVideo:
                            tt = Tweet.fromHtml(str(t))
                            if tt:
                                if not (not image and not video and tt.content == ""):
                                    d[tt.getKey()] = tt
                                # print(tt)

        # print(len(d.keys()))
        if len(d.keys()) >= count:
            driver.quit()
            return d
        else:
            driver.execute_script("window.scrollTo(0, {0})".format(x * 1500))
            x += 1
            WebDriverWait(driver, 10).until_not(
                EC.presence_of_element_located((By.XPATH, '//div[@role="progressbar"]')))