'''
Module contains all browser related operations and classes
'''

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from constants import BASE_URL, MONTHS
from utils import get_previous_nth_month


class Browser:
    '''
    Class will initiate browser
    '''

    def __init__(
        self, category: str = None, search_phrase: str = None, months: int = 1
    ) -> None:
        self._browser = Selenium()
        self._driver = None  # Initially browser is not open
        self._category = category
        self._search_phrase = search_phrase
        self._months = months
        self._threshold_month, self._threshold_year = get_previous_nth_month(
            self._months
        )
        self._url = self._build_url()

    @property
    def browser(self) -> Selenium:
        '''
        This getter will return browser for manual workings
        '''

        return self._browser

    @property
    def driver(self) -> Selenium:
        '''
        This getter will return driver for manual workings
        '''

        return self._driver

    def open_browser(self):
        '''
        Open available browser and visit given url
        '''

        self._browser.open_available_browser(self._url)

    def _build_url(self) -> str:
        '''
        We are scraping al jazeera which has no option of category
        So we will prioritize search phrase at first else category
        if both are not available we will look for breaking news
        '''

        if self._search_phrase:
            return f'{BASE_URL}search/{self._search_phrase}?sort=date'
        elif self._category:
            return f'{BASE_URL}search/{self._category}?sort=date'

        return f'{BASE_URL}search/breaking?sort=date'

    def search_news(self) -> list:
        '''
        This method will execute if news is search through search phrase
        '''

        self._driver = self._browser.driver
        news_set = set()

        if (
            self._driver.find_element(By.CLASS_NAME, 'search-summary__query')
            == 'About 0 results'
        ):
            # return empty list if no matchings found
            return []

        self._driver.find_element(By.CLASS_NAME, 'search-result__list')

        while True:
            try:
                article_elements = self._driver.find_elements(
                    By.TAG_NAME,
                    'article',
                )
                for article in article_elements:

                    (
                        published_time,
                        title,
                        description,
                        image_url,
                    ) = Browser._news_details(article)

                    valid_article = self._is_valid_article(published_time)
                    phrase_count = Browser._count_substring_in_texts(
                        self._search_phrase, title, description
                    )

                    if valid_article:
                        news_set.add(
                            (
                                published_time,
                                title,
                                description,
                                phrase_count,
                                image_url,
                            )
                        )
                    else:
                        return list(news_set)
                self._driver.execute_script(
                    'window.scrollTo(0, document.body.scrollHeight);'
                )
                show_more_button = self._driver.find_element(
                    By.XPATH,
                    '//button[@class="show-more-button grid-full-width" and @data-testid="show-more-button"]',  # noqa
                )

                if not show_more_button:
                    break
                show_more_button.click()
            except Exception:
                pass

        return list(news_set)

    def _is_valid_article(self, published_time: str) -> bool:
        '''
        Method checks validity of article according to timestamps
        '''
        valid_article = True
        if 'ago' not in published_time:
            article_year = int(published_time.split(',')[1][-4:])
            article_month = MONTHS[published_time.split(',')[0][:3]]

            valid_article = (
                self._threshold_year <= article_year
                and self._threshold_month <= article_month
            )

        return valid_article

    @staticmethod
    def _news_details(article: WebElement) -> tuple:
        title = article.find_element(By.TAG_NAME, 'h3').text
        published_time, description, *_ = article.find_element(
            By.TAG_NAME, 'p'
        ).text.split(' ... ')
        image_url = article.find_element(
            By.TAG_NAME,
            'img',
        ).get_attribute('src')

        return published_time, title, description, image_url

    @staticmethod
    def _count_substring_in_texts(substring: str, *texts) -> int:
        # Convert the substring to lowercase for case-insensitive matching
        substring_lower = substring.lower()

        # Count occurrences of the substring in each text
        count = 0
        for text in texts:
            count += text.lower().count(substring_lower)

        return count
