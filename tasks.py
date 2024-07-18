from robocorp.tasks import task

from browser import Browser
from excel import ExcelFile


@task
def task(search_string: str, category: str, months: int):
    browser = Browser(category, search_string, months)
    browser.open_browser()
    news_list = browser.search_news()

    excel = ExcelFile('news_list')
    excel.save_data(news_list)
