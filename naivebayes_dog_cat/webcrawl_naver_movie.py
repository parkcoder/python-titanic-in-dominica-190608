from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

class WebCrawlModel:
    def __init__(self):
        pass

    def create_model(self):
        context = './data/'
        driver = webdriver.Chrome(context + 'chromedriver')
        driver.get('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        all_divs = soup.find_all('div', attrs={'class', 'tit3'})
        products = [div.a.string for div in all_divs]
        for product in products:
            movies = product
            print(product)
        driver.close()
        return movies
