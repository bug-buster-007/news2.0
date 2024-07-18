from robocorp.tasks import task

from browser import Browser


@task
def task(search_string: str, category: str, months: int):
    browser = Browser(category, search_string, months)
    browser.open_browser()
    browser.search_news()
